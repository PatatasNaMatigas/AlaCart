# dataManager/CheckoutManager.py

from dataManager.DataModels import (
    ShoppingCart,
    Orders,
    Transactions,
    Items,
    Accounts,
    createItemEntry
)
from ui.Codes import ReturnCode
from ui.main import App
from util.Utils import warn, log, logData, wtf


class CheckoutManager:
    """
    Handles the full checkout pipeline for a buyer.

    Flow:
        1. Validate Cart        - Ensure cart is not empty
        2. Validate Stock       - Ensure all items have sufficient inventory
        3. Create Pending Order - Snapshot the cart into a formal Order
        4. Process Payment      - Validate payment amount and method
        5. Record Transaction   - Persist the transaction record
        6. Update Inventory     - Deduct purchased quantities from stock
        7. Update Seller Stats  - Increment seller's items_sold and amount_earned
        8. Update Buyer Stats   - Increment buyer's items_purchased and amount_spent
        9. Complete Order       - Mark the order as PAID then COMPLETED
       10. Clear Cart           - Empty the buyer's cart after success
    """

    class CheckoutResult:
        """
        Wraps the outcome of a checkout attempt.
        """
        def __init__(self, success: bool, code: ReturnCode, message: str = "",
                     total: int=0, order: dict = None, transaction: dict = None):
            self.success     = success
            self.code        = code
            self.message     = message
            self.total       = total
            self.order       = order or {}
            self.transaction = transaction or {}

        def __repr__(self):
            return (
                f"CheckoutResult("
                f"success={self.success}, "
                f"code={self.code}, "
                f"message='{self.message}', "
                f"order_id={self.order.get('order_id', 'N/A')}, "
                f"transaction_id={self.transaction.get('transaction_id', 'N/A')})"
            )

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(
        self,
        account:      dict,
    ):
        """
        Args:
            account          : The logged-in buyer's profile dict
            items_mgr        : An Items() instance (shared inventory manager)
            accounts_mgr     : An Accounts() instance (for stat updates)
        """
        self.account         = account

        # Initialize cart and orders tied to this account
        self.cart_mgr    = ShoppingCart(account)
        self.order_mgr   = Orders(account)
        self.txn_mgr     = Transactions()

    # ------------------------------------------------------------------
    # Public Entry Point
    # ------------------------------------------------------------------

    def checkout(
        self,
        pay_amount:     float,
        payment_method: Transactions.PaymentMethods
    ) -> "CheckoutManager.CheckoutResult":
        """
        Executes the full checkout pipeline.

        Args:
            pay_amount     : Amount the buyer is paying
            payment_method : A Transactions.PaymentMethods enum value

        Returns:
            CheckoutResult
        """

        # ── Step 1: Validate Cart ──────────────────────────────────────
        cart_items = self.cart_mgr.getCart()
        if not cart_items:
            warn("Checkout attempted with empty cart", "CHECKOUT")
            return self.CheckoutResult(
                success=False,
                code=ReturnCode.CART_EMPTY,
                message="Cart is empty. Add items before checking out."
            )

        log("Cart validated.", "CHECKOUT")

        # ── Step 2: Convert cart items to transaction-compatible format ─
        #    ShoppingCart stores: { item_id, name, quantity, price }
        #    Orders/Transactions need: { item_id, name, quantity,
        #                                price_at_purchase, sub_total }
        order_items = self._convertCartItems(cart_items)

        # ── Step 3: Validate Stock ─────────────────────────────────────
        stock_check = self._validateStock(order_items)
        if stock_check is not None:
            return stock_check

        log("Stock validated.", "CHECKOUT")

        # ── Step 4: Calculate Total ────────────────────────────────────
        total_amount = sum(item["sub_total"] for item in order_items)

        # ── Step 5: Validate Payment Amount ───────────────────────────
        if pay_amount < total_amount:
            warn(
                f"Insufficient payment: paid {pay_amount}, total {total_amount}",
                "CHECKOUT"
            )
            return self.CheckoutResult(
                success=False,
                code=ReturnCode.INSUFFICIENT_PAYMENT,
                message=(
                    f"Insufficient payment: paid {pay_amount}, total {total_amount}"
                )
            )

        log(f"Payment validated. Total: {total_amount:.2f}, Paid: {pay_amount:.2f}", "CHECKOUT")

        # ── Step 6: Create Pending Order ───────────────────────────────
        order = self.order_mgr.createOrder(
            items=order_items,
            status=Orders.Status.PENDING
        )
        log(f"Order created: {order['order_id']}", "CHECKOUT")

        # ── Step 7: Record Transaction ─────────────────────────────────
        self.txn_mgr.recordTransaction(
            items=order_items,
            payAmount=pay_amount,
            paymentMethod=payment_method,
            buyer=App.customerScenes["CustomerHome"]["account"]["username"]
        )
        # Fetch the latest transaction (just recorded)
        all_transactions = self.txn_mgr.getTransactions()
        recorded_txn = all_transactions[-1] if all_transactions else {}
        log(f"Transaction recorded: {recorded_txn.get('transaction_id', 'N/A')}", "CHECKOUT")

        # ── Step 8: Update Inventory ───────────────────────────────────
        self._deductStock(order_items)
        log("Inventory updated.", "CHECKOUT")

        # ── Step 9: Update Buyer Stats ─────────────────────────────────
        items_purchased = sum(cart_items.values())
        log(items_purchased)
        Accounts().modifyAccount(
            username=self.account["username"],
            itemsPurchased=items_purchased,
            incrementItemsPurchased=True,
            amountSpent=total_amount,
            incrementAmountSpent=True,
            balance=total_amount,
            decrementBalance=True
        )
        log(f"Buyer stats updated for '{self.account['username']}'.", "CHECKOUT")

        # ── Step 10: Update Seller Stats (optional) ────────────────────
        seller_updates = {}
        for item in order_items:
            owner = item.get("owner")
            if not owner:
                continue

            if owner not in seller_updates:
                seller_updates[owner] = {"items": 0, "amount": 0.0}

            seller_updates[owner]["items"] += item["quantity"]
            seller_updates[owner]["amount"] += item["sub_total"]

        for seller_username, stats in seller_updates.items():
            Accounts().modifyAccount(
                username=seller_username,
                itemsSold=stats["items"],
                incrementItemsSold=True,
                amountEarned=stats["amount"],
                incrementAmountEarned=True,
                balance=stats["amount"],
                incrementBalance=True
            )
            log(f"Seller stats updated for '{seller_username}': +{stats['items']} items, +{stats['amount']:.2f} earned.",
                "CHECKOUT")

        # ── Step 11: Mark Order as PAID then COMPLETED ─────────────────
        self.order_mgr.modifyOrder(
            order["order_id"],
            status=Orders.Status.PAID
        )
        self.order_mgr.modifyOrder(
            order["order_id"],
            status=Orders.Status.COMPLETED
        )
        log(f"Order {order['order_id']} marked COMPLETED.", "CHECKOUT")

        # ── Step 12: Clear Cart ────────────────────────────────────────
        self._clearCart(cart_items)
        log("Cart cleared.", "CHECKOUT")

        logData(f"Checkout successful for '{self.account['username']}' {recorded_txn}", "CHECKOUT")

        return self.CheckoutResult(
            success=True,
            code=ReturnCode.SUCCESS,
            message="Checkout completed successfully.",
            total=total_amount,
            order=order,
            transaction=recorded_txn
        )

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _convertCartItems(self, cart_items: dict) -> list:
        """
        Converts ShoppingCart items to the format expected by
        Orders and Transactions.

        ShoppingCart format:
            { item_id, name, quantity, price }
            (note: 'price' here is the per-item price, NOT subtotal)

        Target format (createItemEntry):
            { item_id, name, quantity, price_at_purchase, sub_total }
        """
        converted = []
        for cart_item in cart_items:
            item_id  = int(cart_item.split(":")[-1])
            quantity = cart_items[cart_item]

            inventory_item = Items().getItem(item_id)
            if not inventory_item:
                price_at_purchase = cart_item.get("price", 0.0)
            else:
                price_at_purchase = inventory_item["price"]

            converted.append(
                createItemEntry(
                    itemId=item_id,
                    itemName=inventory_item.get("name"),
                    quantity=quantity,
                    priceAtPurchase=price_at_purchase,
                    owner=inventory_item.get("owner")
                )
            )
        return converted

    def _validateStock(self, order_items: list) -> "CheckoutManager.CheckoutResult | None":
        """
        Checks that every item in the order has sufficient stock.

        Returns:
            CheckoutResult if validation fails, None if all stock is sufficient.
        """
        for item in order_items:
            inventory_item = Items().getItem(item["item_id"])

            if not inventory_item:
                warn(f"Item {item['item_id']} not found in inventory", "CHECKOUT")
                return self.CheckoutResult(
                    success=False,
                    code=ReturnCode.ITEM_NOT_FOUND,
                    message=f"Item '{item['name']}' (ID: {item['item_id']}) no longer exists."
                )

            if inventory_item["stock"] < item["quantity"]:
                warn(
                    f"Insufficient stock for item {item['item_id']}: "
                    f"requested {item['quantity']}, available {inventory_item['stock']}",
                    "CHECKOUT"
                )
                return self.CheckoutResult(
                    success=False,
                    code=ReturnCode.INSUFFICIENT_STOCK,
                    message=(
                        f"Not enough stock for '{item['name']}'. "
                        f"Requested: {item['quantity']}, "
                        f"Available: {inventory_item['stock']}."
                    )
                )
        return None

    def _deductStock(self, order_items: list) -> None:
        """
        Deducts purchased quantities from the Items inventory.
        """
        for item in order_items:
            inventory_item = Items().getItem(item["item_id"])
            if inventory_item:
                new_stock = inventory_item["stock"] - item["quantity"]
                Items().modifyItem(
                    itemId=item["item_id"],
                    stock=new_stock
                )

    def _clearCart(self, cart_items: list) -> None:
        """
        Removes all items from the buyer's cart after successful checkout.
        """
        for item_key in cart_items:
            try:
                self.cart_mgr.deleteItem(item_key)
            except (IndexError, ValueError) as e:
                warn(f"Could not parse ID from key '{item_key}': {e}", "CHECKOUT")