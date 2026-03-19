import os, json
import shutil

import os
from glob import glob

from dataManager import DataModels
from datetime import datetime

from util.Utils import wtf, log


def initDatabaseStructure() -> None:
    try:
        os.mkdir("../Database")
    except FileExistsError:
        pass
    try:
        os.mkdir("../Database/summaries")
    except FileExistsError:
        pass
    try:
        os.mkdir("../Database/accounts")
    except FileExistsError:
        pass
    try:
        os.mkdir("../Database/images")
    except FileExistsError:
        pass

    metaFile = "../Database/meta.json"
    if not os.path.exists(metaFile) or os.path.getsize(metaFile) == 0:
        data = {
            "next_item_id" : 0,
            "next_account_id" : 0,
            "next_transaction_id" : 0,
            "next_order_id" : 0
        }
        safeWrite(metaFile, data)

    safeCreateFile("../Database/items.json")
    safeCreateFile("../Database/accounts/accounts.json")

def getItems() -> list:
    return read("../Database/items.json")

def updateItems(data: list) -> None:
    safeWrite("../Database/items.json", data)

def prepareTransactionRecord(buyer: str, items: list, totalPrice: float, payAmount: float, change: float, paymentMethod: DataModels.Transactions.PaymentMethods) -> dict:
    date = datetime.now().date()
    id = autoIncrement(DataModels.ID.TRANSACTION)
    transactionId = f"T{"0" * (9 - len(str(id)))}{id}"
    date = f"{date} {datetime.now().time()}"
    data = {
        "transaction_id" : transactionId,
        "date_time"      : date,
        "buyer"          : buyer,
        "items_summary"  : items,
        "total_price"    : totalPrice,
        "pay_amount"     : payAmount,
        "change"         : change,
        "payment_method" : paymentMethod.value
    }

    return data

def getTransactions(allTime=False) -> list:
    base_path = "../Database/summaries"

    if allTime:
        allRecords = []
        filePattern = os.path.join(base_path, "**", "transactions.json")
        for file_path in glob(filePattern, recursive=True):
            data = read(file_path)
            if isinstance(data, list):
                allRecords.extend(data)
        return allRecords

    date = datetime.now().date()
    today_path = f"{base_path}/{date.year}/{date.month}/{date.day}"

    os.makedirs(today_path, exist_ok=True)
    fullFilePath = f"{today_path}/transactions.json"
    safeCreateFile(fullFilePath, True)

    return read(fullFilePath)


def updateTransactions(data: list) -> None:
    date = datetime.now().date()
    safeWrite(f"../Database/summaries/{date.year}/{date.month}/{date.day}/transactions.json", data)

def getAccounts() -> list:
    return read("../Database/accounts/accounts.json")

def getAccount(username: str) -> dict:
    return read(f"../Database/accounts/{username}/profile.json")

def updateAccounts(data: list) -> None:
    safeWrite("../Database/accounts/accounts.json", data, )

def updateAccount(username: str, data: dict) -> None:
    safeWrite(f"../Database/accounts/{username}/profile.json", data)

def createAccount(data: dict) -> None:
    folder = f"../Database/accounts/{data["username"]}"
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    safeWrite(folder + "/profile.json", data)
    safeCreateFile(folder + "/shoppingCart.json", False)
    safeCreateFile(folder + "/orders.json")

def getOrders(username: str) -> list:
    return read(f"../Database/accounts/{username}/orders.json")

def updateOrders(username: str, data: list) -> None:
    safeWrite(f"../Database/accounts/{username}/orders.json", data)

def getCart(username: str) -> dict:
    return read(f"../Database/accounts/{username}/shoppingCart.json")

def updateCart(username: str, data: dict) -> None:
    safeWrite(f"../Database/accounts/{username}/shoppingCart.json", data)

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
            case DataModels.ID.ORDER:
                nextId = ids["next_order_id"] + 1
                ids["next_order_id"] = nextId
    safeWrite("../Database/meta.json", ids)
    return nextId

def createFile(filename: str, isList: bool=False) -> None:
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(list() if isList else dict(), file, indent=4)

    os.replace(temp_file, filename)

def safeCreateFile(filename: str, isList: bool=False) -> None:
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        temp_file = filename + ".tmp"

        with open(temp_file, "w") as file:
            json.dump(list() if isList else dict(), file, indent=4)

        os.replace(temp_file, filename)

def changeFileName(base: str, oldName: str, newName: str) -> None:
    try:
        os.rename(os.path.join(base, oldName), os.path.join(base, newName))
    except:
        wtf(f"File/Directory with the name {newName} already exists", "CHANGE FILE NAME")

def deleteFile(filename: str) -> None:
    try:
        shutil.rmtree(filename)
    except PermissionError:
        wtf("Folder cannot be deleted", "DELETE FILE NAME")

def clone(source: str, destination: str) -> None:
    try:
        shutil.copy2(source, destination)
    except PermissionError:
        wtf("Folder cannot be cloned", "CLONE FILE NAME")

def replace(source: str, destination: str) -> None:
    os.replace(source, destination)

def safeWrite(filename: str, data: object) -> None:
    temp_file = filename + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)

    os.replace(temp_file, filename)

def read(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        wtf(f"File named {filename} not found! Attempting file creation...")
        safeCreateFile(filename)
        log("Creation Successful")
        with open(filename, "r") as file:
            return json.load(file)