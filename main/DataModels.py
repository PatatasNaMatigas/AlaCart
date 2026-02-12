import FileHandler as FH
from enum import Enum

class ID(Enum):
    ITEM        = 0
    ACCOUNT     = 1
    TRANSACTION = 2
    RECEIPT     = 3

class Items:
    """
        Structure:
        [
            {
                id    : autoIncrement(ID.Items),    (int)
                name  : "",                         (str)
                price : 0.0,                        (float)
                stock : 0,                          (int)
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

    def modifyItem(self, id: int, name: str = None, price: float = None,
                   stock: int = None, tags: list = None, replace: bool = False):
        for item in self.items:
            if item["id"] == id:
                if name is not None:
                    item["name"] = name
                if price is not None:
                    item["price"] = price
                if stock is not None:
                    item["stock"] = stock
                if tags is not None:
                    if replace:
                        item["tags"] = tags
                    else:
                        item["tags"].extend(tags)
                FH.updateItems(self.items)
                return item
        raise ValueError(f"Item with id {id} not found")

    def getItem(self, id: int) -> dict:
        for i in range(len(self.items)):
            if self.items[i]["id"] == id:
                return self.items[i]
        raise ValueError(f"Item with id {id} not found")

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
            receipt_id     : R00001,                     (str)
            date_time      : YYYY-MM-DDTHH:MM:SS,        (str: ISO)
            items_summary  : [                           (list)
                {
                    "item_id"  : 1,
                    "quantity" : 19
                },...
            ],
            total_price    : 0.0                         (float)
        }
    ]
    """

    def __init__(self):
        self.transactions = []
        pass

    def recordTransaction(self, items: list, totalPrice: float) -> None:
        record = FH.prepareTransactionRecord(items, totalPrice)
        self.transactions = FH.loadTransactions()
        self.transactions.append(record)
        FH.updateTransactions(self.transactions)

    def getTransaction(self, transaction_id: str) -> dict:
        for i in range(len(self.transactions)):
            if self.transactions[i]["transaction_id"] is transaction_id:
                return self.transactions[i]
        raise ValueError(f"Item with id {id} not found")

    def getTransactions(self) -> list:
        return self.transactions

class Accounts:

    def __init__(self):
        self.accounts = []