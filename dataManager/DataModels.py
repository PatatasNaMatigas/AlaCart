import datetime

from dataManager import FileHandler as FH
from enum import Enum

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
    ORDER      = 3

class Items:
    """
        Structure:
        [
            {
                id    : autoIncrement(ID.Items)     (int)
                name  : ""                          (str)
                price : 0.0                         (float)
                stock : 0                           (int)
                tags  : [                           (list)
                    "", "", "", "", ...
                ]
            }
        ]
    """

    def __init__(self):
        self.items = FH.loadItems()

    def addItem(self, name: str, price: float, stock: int, tags: list) -> dict:
        data = {
            "id"    : FH.autoIncrement(ID.ITEM),
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
            if item["id"] == itemId:
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
        raise ValueError(f"Item with id {itemId} not found")

    def getItem(self, itemId: int) -> dict:
        for item in self.items:
            if item["id"] == itemId:
                return item
        raise ValueError(f"Item with id {itemId} not found")

    def getItems(self) -> list:
        return self.items

    def deleteItem(self, id: int) -> int:
        for i in range(len(self.items)):
            if self.items[i]["id"] == id:
                del(self.items[i])
                FH.updateItems(self.items)
                return 0
        return 1

class Transactions:

    """
    Structure:
    [
        {
            transaction_id : T00001,                     (str)
            date_time      : YYYY-MM-DDTHH:MM:SS,        (str: ISO)
            items_summary  : [                           (list)
                {
                    "item_id"           : 1,
                    "item_name"         : "Coke",
                    "quantity"          : 67,
                    "price_at_purchase" : 6.7,
                    "subtotal"          : 448.9
                },...
            ],
            total_price    : 0.0,                        (float)
            pay_amount     : 10.0,                       (float)
            change         : 5.0,                        (float)
            payment_method : CASH                        (str: PaymentMethods)
        }
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

    def __init__(self):
        self.transactions = FH.loadTransactions()
        pass

    def recordTransaction(self, items: list, payAmount: float, paymentMethod: PaymentMethods) -> None:
        totalPrice = 0
        for item in items:
            totalPrice += item["sub_total"]
        change = payAmount - totalPrice
        record = FH.prepareTransactionRecord(items, totalPrice, payAmount, change, paymentMethod)
        self.transactions = FH.loadTransactions()
        self.transactions.append(record)
        FH.updateTransactions(self.transactions)

    def getTransaction(self, transactionId: str) -> dict:
        for i in range(len(self.transactions)):
            print(self.transactions[i]["transaction_id"])
            if self.transactions[i]["transaction_id"] == transactionId:
                return self.transactions[i]
        raise ValueError(f"Transaction with id {transactionId} not found")

    def getTransactions(self) -> list:
        return self.transactions

class Accounts:

    """
    Structure:
    [
        {
            user_id  : 1                   (int)
            username : ""                  (str)
            password : ""                  (str)
            stats    : {
                items_purchased : 1        (int)
            }
        }
    ]
    """

    def __init__(self):
        self.accounts = FH.loadAccounts()

    def createAccount(self, username: str, password: str) -> dict:
        for account in self.accounts:
            if account["username"].strip().lower() == username.strip().lower():
                raise ValueError(f"Username '{username}' already exists")
        profile = {
            "user_id"  : FH.autoIncrement(ID.ACCOUNT),
            "username" : username,
            "password" : password,
            "stats"    : {
                "items_purchased" : 0,
                "amount_spent"    : 0
            }
        }
        self.accounts.append(profile)
        FH.updateAccounts(self.accounts)
        FH.createAccount(profile)
        return profile

    def getAccount(self, userId: int) -> dict:
        for account in self.accounts:
            if account["user_id"] == userId:
                return account
        raise ValueError(f"Account with id {userId} not found")

    def getAccounts(self):
        return self.accounts

    def modifyAccount(self, userId: int, username: str = None, password: str = None, itemsPurchased: int = None, amountSpent: int = None) -> dict:
        for account in self.accounts:
            if account["user_id"] == userId:
                account["username"] = username if username is not None else account["username"]
                account["password"] = password if password is not None else account["password"]
                account["stats"]["items_purchased"] = itemsPurchased if itemsPurchased is not None else account["stats"]["items_purchased"]
                account["stats"]["amount_spent"] = amountSpent if amountSpent is not None else account["stats"]["amount_spent"]
                FH.updateAccounts(self.accounts)
                return account
        raise ValueError(f"Account with id {userId} not found")

    def deleteAccount(self, userId: int) -> None:
        for i in range(len(self.accounts)):
            if self.accounts[i]["user_id"] == userId:
                del(self.accounts[i])
                return
        raise ValueError(f"Account with id {userId} not found")

class Orders:

    """
    Structure:
    [
        {
            order_id        : str
            created_at      : ISO datetime string
            items           : list[OrderItem]
            total_amount    : float
            status          : str (enum)
        }
    ]
    """

    class Status(Enum):
        PENDING   = 0
        PAID      = 1
        CANCELLED = 2
        EXPIRED   = 3
        COMPLETED = 4

    def __init__(self, account: dict):
        self.username = account["username"]
        self.orders = FH.loadOrders(self.username)

    def getOrders(self) -> list:
        return self.orders

    def createOrder(self, items: list, status: Status) -> dict:
        totalAmount = 0
        for item in items:
            totalAmount += item["sub_total"]
        return {
            "order_id"     : FH.autoIncrement(ID.ORDER),
            "date_time"    : datetime.datetime.now().isoformat(),
            "items"        : items,
            "total_amount" : totalAmount,
            "status"       : status
        }

    def modifyOrder(self, orderId: int, items: list = None, status: Status = None) -> dict:
        newTotal = 0
        if items is not None:
            for item in items:
                newTotal += item["sub_total"]
        for order in self.orders:
            if order["order_id"] == orderId:
                order["items"] = items if items is not None else order["items"]
                order["total_amount"] = newTotal if items is not None else order["total_amount"]
                order["status"] = status if status is not None else ["status"]
                return order
        raise ValueError(f"Order with id {orderId} not found")

    def updateOrders(self, data: list) -> None:
        FH.updateOrders(self.username, data)