from util.Utils import log, logbr, warn, wtf
from dataManager import FileHandler as FH, DataModels
from dataManager.DataModels import Items, Transactions, Accounts, Orders

FH.initDatabaseStructure()
#
# items = Items()
# items.addItem(
#     "XO Coffee Candy 50 pcs.",
#     50.0,
#     10,
#     ["candy", "coffee"]
# )
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
# items.addItem(
#     "balipure water 350ml",
#     10,
#     10,
#     ["water", "purified drinking water", "drinking water", "350ml"]
# )
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
# items.modifyItem(
#     2,
#     stock=6
# )
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
# items.deleteItem(1)
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
# items.modifyItem(
#     2,
#     tags=["350ML"],
#     replace=True
# )
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
# items.modifyItem(
#     2,
#     tags=["Purified Drinking Water"],
#     replace=False
# )
# print(items.getItems())
# print("---------------------------------------------------------------------------------------------")
#
# transactions = Transactions()
# transactions.recordTransaction(
#     [
#         DataModels.createItemEntry(
#             1,
#             "Coke",
#             10,
#             72.50
#         ),
#         DataModels.createItemEntry(
#             2,
#             "XO Candy Coffee",
#             200,
#             47.60
#         )
#     ],
#     11000.00,
#     Transactions.PaymentMethods.MLBB_DIAMONDS
#
# )
# print(transactions.getTransactions())
# print("---------------------------------------------------------------------------------------------")
#
# accounts = Accounts()
# username = "Aee"
# password = "SomePassword"
# try:
#     accounts.createAccount(username, password)
# except ValueError:
#     wtf(f"Account \"{username}\" already exists!")
#     logbr()
#
# log(accounts.getAccounts())
# logbr()
# accounts.modifyAccount(
#     1,
#     password="Eticles"
# )
# log(accounts.getAccounts())
# logbr()
#
# orders = Orders(accounts.getAccount(1))
# log(orders.getOrders())
# logbr()
#
# order = orders.createOrder(
#     [
#         DataModels.createItemEntry(
#             1,
#             "Coke",
#             10,
#             72.50
#         ),
#         DataModels.createItemEntry(
#             2,
#             "XO Candy Coffee",
#             200,
#             47.60
#         )
#     ],
#     Orders.Status.PENDING
# )
# log(orders.getOrders())
# logbr()
# orders.completeOrder(accounts, 1)
