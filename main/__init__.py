import FileHandler as FH
from DataModels import Items, Transactions

FH.initDatabaseStructure()

items = Items()
items.addItem(
    "XO Coffee Candy 50 pcs.",
    50.0,
    10,
    ["candy", "coffee"]
)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")
items.addItem(
    "balipure water 350ml",
    10,
    10,
    ["water", "purified drinking water", "drinking water", "350ml"]
)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")
items.modifyItem(
    2,
    stock=6
)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")
items.deleteItem(1)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")
items.modifyItem(
    2,
    tags=["350ML"],
    replace=True
)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")
items.modifyItem(
    2,
    tags=["Purified Drinking Water"],
    replace=False
)
print(items.getItems())
print("---------------------------------------------------------------------------------------------")

transactions = Transactions()
transactions.recordTransaction([{"item_id" : 3, "quantity" : 4}, {"item_id" : 5, "quantity" : 6}, {"item_id" : 7, "quantity" : 8}], 679.67)
print(transactions.getTransactions())
print("---------------------------------------------------------------------------------------------")
transactions.recordTransaction([{"item_id" : 1, "quantity" : 9}, {"item_id" : 7, "quantity" : 5}], 1975)
print(transactions.getTransactions())
print("---------------------------------------------------------------------------------------------")