import os, json
from dataManager import DataModels
from datetime import datetime

def initDatabaseStructure() -> None:
    try:
        os.mkdir("../Database")
        os.mkdir("../Database/summaries")
        os.mkdir("../Database/accounts")
        os.mkdir("../Database/temp")
    except FileExistsError:
        pass

    metaFile = "../Database/meta.json"
    if not os.path.exists(metaFile) or os.path.getsize(metaFile) == 0:
        data = {
            "next_item_id" : 0,
            "next_account_id" : 0,
            "next_transaction_id" : 0,
        }
        safeWrite(metaFile, data)

    safeCreateFile("../Database/items.json")
    safeCreateFile("../Database/accounts/accounts.json")

def loadItems() -> list:
    return read("../Database/items.json")

def updateItems(data: list) -> None:
    safeWrite("../Database/items.json", data)

def prepareTransactionRecord(items: list, totalPrice: float, payAmount: float, change: float, paymentMethod: DataModels.Transactions.PaymentMethods) -> dict:
    date = datetime.now().date()
    id = autoIncrement(DataModels.ID.TRANSACTION)
    transactionId = f"T{"0" * (9 - len(str(id)))}{id}"
    date = f"{date} {datetime.now().time()}"
    data = {
        "transaction_id" : transactionId,
        "date_time"      : date,
        "items_summary"  : items,
        "total_price"    : totalPrice,
        "pay_amount"     : payAmount,
        "change"         : change,
        "payment_method" : paymentMethod.value
    }

    return data

def loadTransactions() -> list:
    date = datetime.now().date()
    try:
        os.mkdir(f"../Database/summaries/{date.year}")
        os.mkdir(f"../Database/summaries/{date.year}/{date.month}")
        os.mkdir(f"../Database/summaries/{date.year}/{date.month}/{date.day}")
    except FileExistsError:
        pass

    safeCreateFile(f"../Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json")
    date = datetime.now().date()
    return read(f"../Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json")

def updateTransactions(data: list) -> None:
    date = datetime.now().date()
    safeWrite(f"../Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json", data)

def loadAccounts() -> list:
    return read("../Database/accounts/accounts.json")

def updateAccounts(data: list) -> None:
    safeWrite("../Database/accounts/accounts.json", data)

def createAccount(data: dict) -> None:
    folder = f"../Database/accounts/{data["username"]}"
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    safeWrite(folder + "/profile.json", data)
    safeCreateFile(folder + "/shoppingCart.json")
    safeCreateFile(folder + "/orders.json")

def autoIncrement(idType: DataModels.ID) -> int:
    nextId = 0
    with open("../Database/meta.json", 'r+') as file:
        ids = json.load(file)
        match idType:
            case DataModels.ID.ITEM:
                nextId = ids["next_item_id"] + 1
                ids["next_item_id"] = nextId
            case DataModels.ID.ACCOUNT:
                nextId = ids["next_account_id"] + 1
                ids["next_account_id"] = nextId
            case DataModels.ID.TRANSACTION:
                nextId = ids["next_transaction_id"] + 1
                ids["next_transaction_id"] = nextId
            case DataModels.ID.RECEIPT:
                nextId = ids["next_receipt_id"] + 1
                ids["next_receipt_id"] = nextId
    safeWrite("../Database/meta.json", ids)
    return nextId

def safeWrite(filename, data) -> None:
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)

    os.replace(temp_file, filename)

def createFile(filename) -> None:
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump([], file, indent=4)

    os.replace(temp_file, filename)

def safeCreateFile(filename) -> None:
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        temp_file = filename + ".tmp"

        with open(temp_file, "w") as file:
            json.dump([], file, indent=4)

        os.replace(temp_file, filename)

def read(filename) -> list:
    with open(filename, "r") as file:
        return json.load(file)