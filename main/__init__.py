from util.Utils import log, logbr, warn, wtf, logData
from dataManager import FileHandler as FH, DataModels
from dataManager.DataModels import Items, Transactions, Accounts, Orders

FH.initDatabaseStructure()

items = Items()
items.addItem(
    "XO Coffee Candy 50 pcs.",
    50.0,
    10,
    ["candy", "coffee"]
)
logData(items.getItems(), "ITEMS")
logbr()

items.addItem(
    "balipure water 350ml",
    10,
    10,
    ["water", "purified drinking water", "drinking water", "350ml"]
)
log(items.getItems(), "ITEMS")
logbr()

items.modifyItem(
    2,
    stock=6
)
log(items.getItems(), "ITEMS")
logbr()

items.deleteItem(2)
log(items.getItems(), "ITEMS")
logbr()

items.modifyItem(
    3,
    tags=["350ML"],
    replace=True
)
log(items.getItems(), "ITEMS")
logbr()

items.modifyItem(
    3,
    tags=["Purified Drinking Water"],
    replace=False
)
log(items.getItems(), "ITEMS")
logbr()

transactions = Transactions()
transactions.recordTransaction(
    [
        DataModels.createItemEntry(
            1,
            "Coke",
            10,
            72.50
        ),
        DataModels.createItemEntry(
            2,
            "XO Candy Coffee",
            200,
            47.60
        )
    ],
    11000.00,
    Transactions.PaymentMethods.MLBB_DIAMONDS

)
print(transactions.getTransactions())
print("---------------------------------------------------------------------------------------------")

accounts = Accounts()
username = "Aee"
password = "SomePassword"
try:
    accounts.createAccount(username, password)
except ValueError:
    wtf(f"Account \"{username}\" already exists!")
    logbr()

log(accounts.getAccounts())
logbr()
accounts.modifyAccount(
    1,
    password="Eticles"
)
log(accounts.getAccounts())
logbr()

orders = Orders(accounts.getAccount(1))
log(orders.getOrders())
logbr()

order = orders.createOrder(
    [
        DataModels.createItemEntry(
            1,
            "Coke",
            10,
            72.50
        ),
        DataModels.createItemEntry(
            2,
            "XO Candy Coffee",
            200,
            47.60
        )
    ],
    Orders.Status.PENDING
)
log(orders.getOrders())
logbr()
orders.completeOrder(accounts, 1)
