import datetime

from dataManager import FileHandler as FH
from enum import Enum

from ui.Codes import ReturnCode
from util.Utils import warn, log


def createItemEntry(itemId: int, itemName: str, quantity: int, priceAtPurchase: float, owner: str) -> dict:
    return {
        "item_id"           : itemId,
        "name"              : itemName,
        "quantity"          : quantity,
        "price_at_purchase" : priceAtPurchase,
        "sub_total"         : quantity * priceAtPurchase,
        "owner"             : owner
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

    class Filter(Enum):
        RECENTLY_ADDED = "item_id"
        NAME = "name"
        PRICE = "price"
        STOCK = "stock"

    def __init__(self):
        self.items = FH.getItems()

    def addItem(self, name: str, price: float, stock: int, tags: list, owner: str) -> dict:
        data = {
            "item_id" : FH.autoIncrement(ID.ITEM),
            "name"   : name,
            "price"  : price,
            "stock"  : stock,
            "tags"   : tags,
            "owner"  : owner
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
        for item in FH.getItems():
            if item["item_id"] == itemId:
                return item
        warn(f"Item with id {itemId} not found", "GET ITEM")
        return {}

    def getItems(self, owner: str=None) -> list:
        if owner is None:
            return self.items
        else:
            ownerItems = []
            for item in self.items:
                if item["owner"] == owner:
                    ownerItems.append(item)
            return ownerItems

    def deleteItem(self, itemId: int) -> None:
        for i in range(len(self.items)):
            if self.items[i]["item_id"] == itemId:
                del self.items[i]
                FH.updateItems(self.items)
                return
        warn(f"Item with id {itemId} not found", "DELETE ITEM")

    def sort(self, key: int, ascending=True) -> list:
        match key:
            case 0:
                key = self.Filter.RECENTLY_ADDED.value
                return sorted(self.items, key=lambda item: item[key], reverse=ascending)
            case 1:
                key = self.Filter.STOCK.value
                return sorted(self.items, key=lambda item: item[key], reverse=ascending)
            case 2:
                key = self.Filter.PRICE.value
                return sorted(self.items, key=lambda item: item[key], reverse=ascending)
            case 3:
                key = self.Filter.NAME.value
                return sorted(self.items, key=lambda item: item[key].lower(), reverse=ascending)
        return []

    def exists(self, i: int) -> bool:
        for item in self.items:
            if item["item_id"] == i:
                return True
        return False


class Transactions:

    """
    Structure:
    [
        {
            transaction_id : (str)
            date_time      : (str: ISO),
            buyer          : (str)
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

    def recordTransaction(self, buyer: str, items: list, payAmount: float, paymentMethod: PaymentMethods) -> None:
        totalPrice = 0
        for item in items:
            totalPrice += item["sub_total"]
        change = payAmount - totalPrice
        record = FH.prepareTransactionRecord(buyer, items, totalPrice, payAmount, change, paymentMethod)
        self.transactions = FH.getTransactions()
        self.transactions.append(record)
        FH.updateTransactions(self.transactions)

    def getUserTransactions(self, username: str) -> list:
        allTransactions = FH.getTransactions(True)
        user_records = [tx for tx in allTransactions if tx.get('buyer') == username]
        return user_records[::-1]

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
                "items_purchased" : (int),
                "amount_spent"    : (int),
                "items_sold"      : (int),
                "amount_earned"   : (int),
                "balance"         : (int)
            }
        },
        ...
    ]
    """

    class Role(Enum):
        SELLER = "seller"
        BUYER  = "buyer"

    def __init__(self):
        self.accounts = FH.getAccounts()

    def createAccount(self, username: str, password: str, role: Role) -> tuple:
        self.accounts = FH.getAccounts()
        if not username or not password:
            return tuple(
                code for code, condition in [
                    (ReturnCode.MISSING_USERNAME, not username),
                    (ReturnCode.MISSING_PASSWORD, not password),
                    ({}, True)
                ] if condition
            )

        if not self.checkPassword(password):
            return ReturnCode.PASSWORD_INVALID, {}

        if username in self.accounts:
            return ReturnCode.ACCOUNT_ALREADY_EXISTS, {}

        self.accounts.append(
            username
        )
        FH.updateAccounts(self.accounts)

        profile = {
            "user_id"  : FH.autoIncrement(ID.ACCOUNT),
            "username" : username,
            "password" : password,
            "role"     : role.value,
            "stats"    : {
                "items_purchased" : 0,
                "amount_spent"    : 0,
                "items_sold"      : 0,
                "amount_earned"   : 0,
                "balance"         : 0
            }
        }
        FH.createAccount(profile)

        return ReturnCode.SUCCESS, profile

    def authenticate(self, username: str, password: str) -> ReturnCode | tuple:
        if not username or not password:
            return tuple(
                code for code, condition in [
                    (ReturnCode.MISSING_USERNAME, not username),
                    (ReturnCode.MISSING_PASSWORD, not password)
                ] if condition
            )
        if not username in self.accounts:
            return ReturnCode.ACCOUNT_DOES_NOT_EXIST
        if FH.getAccount(username)["password"] == password:
            return ReturnCode.SUCCESS
        return ReturnCode.PASSWORD_INCORRECT

    def checkPassword(self, password: str) -> ReturnCode:
        if len(password) < 8:
            return ReturnCode.PASSWORD_INVALID
        number = False
        specialCharacter = False
        for c in password:
            if c.isdigit():
                number = True
            if not c.isalnum() and not c.isspace() and not c.isdigit():
                specialCharacter = True
        return ReturnCode.SUCCESS if number and specialCharacter else ReturnCode.PASSWORD_INVALID

    def getRole(self, username: str) -> Role:
        return self.Role(FH.getAccount(username)["role"])

    def modifyAccount(self, username: str, newUsername: str = None, newPassword: str = None,
                      itemsPurchased: int = None, incrementItemsPurchased: bool = False,
                      amountSpent: int = None, incrementAmountSpent: bool = False,
                      itemsSold: int = None, incrementItemsSold: bool = False,
                      amountEarned: int = None, incrementAmountEarned: bool = False,
                      balance: int = None, incrementBalance: bool = False, decrementBalance: bool = False,
                      ) -> None:
        self.accounts = FH.getAccounts()
        if username not in self.accounts:
            warn(f"Account with username \"{username}\" does not exist", "MODIFY ACCOUNT")
            return

        profile = FH.getAccount(username)
        if newUsername is not None:
            profile["username"] = newUsername
        if newPassword is not None:
            profile["password"] = newPassword
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
        if itemsSold is not None:
            if incrementItemsSold:
                profile["stats"]["items_sold"] += itemsSold
            else:
                profile["stats"]["items_sold"] = itemsSold
        if amountEarned is not None:
            if incrementAmountEarned:
                profile["stats"]["amount_earned"] += amountEarned
            else:
                profile["stats"]["amount_earned"] = amountEarned
        if balance is not None:
            if incrementBalance:
                profile["stats"]["balance"] += balance
            elif decrementBalance:
                profile["stats"]["balance"] -= balance
            else:
                profile["stats"]["balance"] = balance
        if newUsername:
            self.accounts.remove(username)
            self.accounts.append(newUsername)
            FH.updateAccounts(self.accounts)
            FH.changeFileName(
                "../Database/accounts/",
                username,
                newUsername
            )
            FH.updateAccount(newUsername, profile)
        else:
            FH.updateAccount(username, profile)

    def deleteAccount(self, username: str) -> None:
        if username not in self.accounts:
            warn(f"Account with username \"{username}\" not found", "DELETE ACCOUNT")
            return

        self.accounts.remove(username)
        FH.updateAccounts(self.accounts)
        FH.deleteFile(f"../Database/accounts/{username}")

    def getAccount(self, username: str) -> dict:
        return FH.getAccount(username)

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
    {
        "itemId:{id: int}"   : "quantity,
        ...
    }
    """

    def __init__(self, account: dict):
        self.cart = FH.getCart(account["username"])
        self.account = account

    def item(self, item: str, quantity: int) -> None:
        self.cart = FH.getCart(self.account["username"])
        self.cart[item] = quantity
        FH.updateCart(self.account["username"], self.cart)

    def getCart(self) -> dict:
        raw_cart = FH.getCart(self.account["username"])

        return {
            key: quantity
            for key, quantity in raw_cart.items()
            if Items().exists(int(key.split(":")[-1]))
        }

    def deleteItem(self, item: str) -> None:
        self.cart = FH.getCart(self.account["username"])
        if item in self.cart:
            self.cart.pop(item)
            FH.updateCart(self.account["username"], self.cart)
            return

        warn(f"Item with id {item} not found", "DELETE ITEM / SHOPPING CART")