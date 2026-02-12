import os, json, DataModels
from datetime import datetime

def initDatabaseStructure() -> None:
    try:
        os.mkdir("Database")
        os.mkdir("Database/summaries")
        os.mkdir("Database/accounts")
        os.mkdir("Database/temp")
    except FileExistsError:
        pass

    metaFile = "Database/meta.json"
    if not os.path.exists(metaFile) or os.path.getsize(metaFile) == 0:
        data = {
            "next_item_id" : 0,
            "next_account_id" : 0,
            "next_transaction_id" : 0,
            "next_receipt_id" : 0,
        }
        safeWrite(metaFile, data)

    itemsFile = "Database/items.json"
    if not os.path.exists(itemsFile) or os.path.getsize(itemsFile) == 0:
        createFile(itemsFile)

def loadItems() -> list:
    return read("Database/items.json")

def updateItems(data: list) -> None:
    safeWrite("Database/items.json", data)

def prepareTransactionRecord(items: list, totalPrice: float) -> dict:
    date = datetime.now().date()
    try:
        os.mkdir(f"Database/summaries/{date.year}")
        os.mkdir(f"Database/summaries/{date.year}/{date.month}")
        os.mkdir(f"Database/summaries/{date.year}/{date.month}/{date.day}")
    except FileExistsError:
        pass

    transactionsFile = f"Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json"
    if not os.path.exists(transactionsFile) or os.path.getsize(transactionsFile) == 0:
        createFile(transactionsFile)

    receiptsFile = f"Database/summaries/{date.year}/{date.month}/{date.day}/receipts.json"
    if not os.path.exists(receiptsFile) or os.path.getsize(receiptsFile) == 0:
        createFile(receiptsFile)

    id = autoIncrement(DataModels.ID.TRANSACTION)
    transactionId = f"T{"0" * (9 - len(str(id)))}{id}"
    receiptId = f"R{"0" * (9 - len(str(id)))}{id}"
    date = f"{date} {datetime.now().time()}"
    data = {
        "transaction_id" : transactionId,
        "receipt_id"     : receiptId,
        "date_time"      : date,
        "items_summary"  : items,
        "total_price"    : totalPrice
    }

    return data

def loadTransactions() -> list:
    date = datetime.now().date()
    return read(f"Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json")

def updateTransactions(data: list) -> None:
    date = datetime.now().date()
    safeWrite(f"Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json", data)

def createAccountFiles(username: str, password: str) -> None:
    folder = f"Database/accounts/{username}"
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    profileFile = folder + "/profile.json"
    data = [
        {
            "user_id"  : autoIncrement(DataModels.ID.ACCOUNT),
            "username" : username,
            "password" : password
        }
    ]
    safeWrite(profileFile, data)
    createFile(folder + "/cart.json")
    createFile(folder + "/orders.json")

def autoIncrement(idType: DataModels.ID) -> int:
    nextId = 0
    with open("Database/meta.json", 'r+') as file:
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
    safeWrite("Database/meta.json", ids)
    return nextId

def safeWrite(filename, data):
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)

    os.replace(temp_file, filename)

def createFile(filename):
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump([], file, indent=4)

    os.replace(temp_file, filename)

def read(filename) -> list:
    with open(filename, "r") as file:
        return json.load(file)