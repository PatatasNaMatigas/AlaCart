import datetime

from dataManager import FileHandler as FH
from enum import Enum

from util.Utils import warn


def createItemEntry(itemId: int, itemName: str, quantity: int, priceAtPurchase: float) -> dict:
    return {
        "item_id"           : itemId,
        "item_name"         : itemName,
        "quantity"          : quantity,
        "price_at_purchase" : priceAtPurchase,
        "sub_total"         : quantity * priceAtPurchase
    }

class ID(Enum):
    ITEM        = 0
    ACCOUNT     = 1
    TRANSACTION = 2
    ORDER       = 3

class Items:
    """
        Structure:
        [
            {
                item_id    : (int)
                name  : (str)
                price : (float)
                stock : (int)
                tags  : [
                    (str),
                    ...
                ]
            },
            ...
        ]
    """

    def __init__(self):
        self.items = FH.getItems()

    def addItem(self, name: str, price: float, stock: int, tags: list) -> dict:
        data = {
            "item_id"    : FH.autoIncrement(ID.ITEM),
            "name"  : name,
            "price" : price,
            "stock" : stock,
            "tags"  : tags
        }
        self.items.append(data)
        FH.updateItems(self.items)
        return data

    def modifyItem(self, itemId: int, name: str = None, price: float = None,
                   stock: int = None, tags: list = None, replace: bool = False) -> dict:
        for item in self.items:
            if item["item_id"] == itemId:
                item["name"] = name if name is not None else item["name"]
                item["price"] = price if price is not None else item["price"]
                item["stock"] = stock if stock is not None else item["stock"]
                if tags is not None:
                    if replace:
                        item["tags"] = tags
                    else:
                        item["tags"].extend(tags)
                FH.updateItems(self.items)
                return item
        warn(f"Item {itemId} not found", "MODIFY ITEM")
        return {}

    def getItem(self, itemId: int) -> dict:
        for item in self.items:
            if item["item_id"] == itemId:
                return item
        warn(f"Item with id {itemId} not found", "GET ITEM")
        return {}

    def getItems(self) -> list:
        return self.items

    def deleteItem(self, itemId: int) -> None:
        for i in range(len(self.items)):
            if self.items[i]["item_id"] == itemId:
                del self.items[i]
                FH.updateItems(self.items)
                return
        warn(f"Item with id {itemId} not found", "DELETE ITEM")

class Transactions:

    """
    Structure:
    [
        {
            transaction_id : (str)
            date_time      : (str: ISO)
            items_summary  : [
                {
                    "item_id"           : (int)
                    "item_name"         : (str)
                    "quantity"          : (int)
                    "price_at_purchase" : (float)
                    "subtotal"          : (float)
                },
                ...
            ],
            total_price    : (float)
            pay_amount     : (float)
            change         : (float)
            payment_method : (PaymentMethods.value)
        },
        ...
    ]
    """

    class PaymentMethods(Enum):
        CASH              = "Cash"
        DEBIT_CARD        = "Debit Card"
        CREDIT_CARD       = "Credit Card"
        BANK_TRANSFER     = "Bank Transfer"
        SPAY_LATER        = "SPayLater"
        KO_FI             = "Ko-Fi"
        GO_FUND_ME        = "GoFundMe"
        MLBB_DIAMONDS     = "MLBB Diamonds"
        ROBUX             = "Robux"
        MINECOINS         = "Minecoins"
        V_BUCKS           = "V Bucks"
        YOUTUBE_THANKS    = "Youtube Thanks"
        TIKTOK_LIVE_GIFTS = "Tiktok Live Gifts"
        GSHOCK            = "G Shock"
        BEEP_CARD         = "Beep Card"

    def __init__(self):
        self.transactions = FH.getTransactions()
        pass

    def recordTransaction(self, items: list, payAmount: float, paymentMethod: PaymentMethods) -> None:
        totalPrice = 0
        for item in items:
            totalPrice += item["sub_total"]
        change = payAmount - totalPrice
        record = FH.prepareTransactionRecord(items, totalPrice, payAmount, change, paymentMethod)
        self.transactions = FH.getTransactions()
        self.transactions.append(record)
        FH.updateTransactions(self.transactions)

    def getTransaction(self, transactionId: str) -> dict:
        for i in range(len(self.transactions)):
            print(self.transactions[i]["transaction_id"])
            if self.transactions[i]["transaction_id"] == transactionId:
                return self.transactions[i]
        warn(f"Transaction with id {transactionId} not found", "GET TRANSACTION")
        return {}

    def getTransactions(self) -> list:
        return self.transactions

class Accounts:

    """
    Structure:
    [
        {
            "user_id"  : (int)
            "username" : (str)
            "password" : (str)
            "stats"    : {
                items_purchased : (int),
                "amount_spent"  : (int),
            }
        },
        ...
    ]
    """

    class Role(Enum):
        OWNER = 1
        CUSTOMER = 2

    def __init__(self):
        self.accounts = FH.getAccounts()

    def createAccount(self, username: str, password: str, role: Role) -> dict:
        if username in self.accounts:
            warn(f"Account with username {username} already exists", "CREATE ACCOUNT")
            return {}

        self.accounts.append(
            username
        )
        FH.updateAccounts(self.accounts)

        profile = {
            "user_id"  : FH.autoIncrement(ID.ACCOUNT),
            "username" : username,
            "password" : password,
            "role"     : role.value,
            "stats": {
                "items_purchased" : 0,
                "amount_spent"    : 0
            }
        }
        FH.createAccount(profile)

        return profile

    def modifyAccount(self, username: str, newUsername: str = None, newPassword: str = None,
                      itemsPurchased: int = None, incrementItemsPurchased: bool = False,
                      amountSpent: int = None, incrementAmountSpent: bool = False) -> None:
        if username not in self.accounts:
            warn(f"Account with username \"{username}\" does not exist", "MODIFY ACCOUNT")
            return

        profile = FH.getAccount(username)
        profile["username"] = newUsername if newUsername is not None else profile["username"]
        profile["password"] = newPassword if newPassword is not None else profile["password"]
        if itemsPurchased is not None:
            if incrementItemsPurchased:
                profile["stats"]["items_purchased"] += itemsPurchased
            else:
                profile["stats"]["items_purchased"] = itemsPurchased
        if amountSpent is not None:
            if incrementAmountSpent:
                profile["stats"]["amount_spent"] += amountSpent
            else:
                profile["stats"]["amount_spent"] = amountSpent
        self.accounts.remove(username)
        self.accounts.append(newUsername)
        FH.updateAccounts(self.accounts)
        FH.changeFileName(
            "../Database/accounts/",
            username,
            newUsername
        )
        FH.updateAccount(newUsername, profile)

    def deleteAccount(self, username: str) -> None:
        if username not in self.accounts:
            warn(f"Account with username \"{username}\" not found", "DELETE ACCOUNT")
            return

        self.accounts.remove(username)
        FH.updateAccounts(self.accounts)
        FH.deleteFile(f"../Database/accounts/{username}")


class Orders:

    """
    Structure:
    [
        {
            order_id        : (str)
            created_at      : (str)
            items           : [
                "item_id"           : (int),
                "item_name"         : (str),
                "quantity"          : (int),
                "price_at_purchase" : (float),
                "sub_total"         : (float)
            ]
            total_amount    : (float)
            status          : (Status.value)
        },
        ...
    ]
    """

    class Status(Enum):
        PENDING   = 0
        PAID      = 1
        CANCELLED = 2
        EXPIRED   = 3
        COMPLETED = 4

    def __init__(self, account: dict):
        self.account = account
        self.orders = FH.getOrders(self.account["username"])

    def getOrders(self) -> list:
        return self.orders

    def createOrder(self, items: list, status: Status) -> dict:
        totalAmount = 0
        for item in items:
            totalAmount += item["sub_total"]
        data = {
            "order_id"     : FH.autoIncrement(ID.ORDER),
            "date_time"    : datetime.datetime.now().isoformat(),
            "items"        : items,
            "total_amount" : totalAmount,
            "status"       : status.value
        }
        self.orders.append(data)
        FH.updateOrders(self.account["username"], self.orders)
        return data

    def modifyOrder(self, orderId: int, items: list = None, status: Status = None) -> dict:
        newTotal = 0
        if items is not None:
            for item in items:
                newTotal += item["sub_total"]
        for order in self.orders:
            if order["order_id"] == orderId:
                order["items"] = items if items is not None else order["items"]
                order["total_amount"] = newTotal if items is not None else order["total_amount"]
                order["status"] = status.value if status is not None else order["status"]
                FH.updateOrders(self.account["username"], self.orders)
                return order
        warn(f"Order with id \"{orderId}\" not found", "MODIFY ORDER")
        return {}

    def completeOrder(self, account: Accounts, orderId: int) -> None:
        for order in self.orders:
            if order["order_id"] == orderId:
                if order["status"] == Orders.Status.COMPLETED.value:
                    warn(f"Order with id \"{orderId}\" has already completed")
                    return
        self.modifyOrder(orderId, status=Orders.Status.COMPLETED)
        FH.updateOrders(self.account["username"], self.orders)

        order = {}
        for o in self.orders:
            if o["order_id"] == orderId:
                order = o

        itemsPurchased = 0
        for item in order["items"]:
            itemsPurchased += item["quantity"]

        amountSpent = order["total_amount"]

        account.modifyAccount(
            self.account["user_id"],
            itemsPurchased=itemsPurchased,
            amountSpent=amountSpent,
            incrementItemsPurchased=True,
            incrementAmountSpent=True
        )

    def getOrder(self, orderId: int) -> dict:
        for order in self.orders:
            if order["order_id"] == orderId:
                return order
        warn(f"Order with id \"{orderId}\" not found", "GET ORDER")
        return {}

class ShoppingCart:

    """
    Structure:
    [
        {
            "item_id"   : (str)
            "item_name" : (str)
            "quantity"  : (int)
            "price"     : (float)
        },
        ...
    ]
    """

    def createItemEntry(self, itemId: int, itemName: str, quantity: int, subtotal: float) -> dict:
        return {
            "item_id"   : itemId,
            "item_name" : itemName,
            "quantity"  : quantity,
            "price"     : subtotal
        }

    def __init__(self, account: dict):
        self.cart = FH.getCart(account["username"])
        self.account = account

    def addItem(self, item: dict) -> None:
        for i in self.cart:
            if i["item_id"] == item["item_id"]:
                i["quantity"] += item["quantity"]
                FH.updateCart(self.account["username"], self.cart)
                return
        self.cart.append(item)
        FH.updateCart(self.account["username"], self.cart)

    def modifyItem(self, itemId: int, quantity: int=None, price: float=None) -> dict:
        for item in self.cart:
            if item["item_id"] == itemId:
                item["quantity"] = quantity if quantity is not None else item["quantity"]
                item["price"] = price if price is not None else item["price"]
                FH.updateCart(self.account["username"], self.cart)
                return item
        warn(f"Item with id \"{itemId}\" not found in the cart", "MODIFY ITEM / SHOPPING CART")
        return {}

    def getItem(self, itemId: int) -> dict:
        for item in self.cart:
            if item["item_id"] == itemId:
                return item
        warn(f"Item with id {itemId} not found", "GET ITEM / SHOPPING CART")
        return {}

    def getCart(self) -> list:
        return self.cart

    def deleteItem(self, itemId: int) -> None:
        for i in range(len(self.cart)):
            if self.cart[i]["item_id"] == itemId:
                del self.cart[i]
                FH.updateCart(self.account["username"], self.cart)
                return
        warn(f"Item with id {itemId} not found", "DELETE ITEM / SHOPPING CART")