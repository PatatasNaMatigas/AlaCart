import os, json
import shutil

import os
import sys
from glob import glob

from dataManager import DataModels
from datetime import datetime

from util.Utils import wtf, log

def resPath(relative):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath("../")
    return os.path.join(base, relative)

def getBaseDir():
    if getattr(sys, 'frozen', False):
        base = os.path.join(os.environ['LOCALAPPDATA'], 'AlaCart')
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    db_path = os.path.join(base, "Database")
    if not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)
    return db_path

DB_BASE = getBaseDir()

import shutil

def initDatabaseStructure() -> None:
    # 1. Create the AppData folders if they don't exist
    subfolders = ["summaries", "accounts", "images"]
    for folder in subfolders:
        os.makedirs(os.path.join(DB_BASE, folder), exist_ok=True)

    # 2. LIST OF FILES TO MIGRATE
    # These are the files you defined in your .spec datas
    files_to_copy = ["items.json", "meta.json"]

    for filename in files_to_copy:
        dest_path = os.path.join(DB_BASE, filename)

        # Only copy if the file doesn't exist in AppData yet
        if not os.path.exists(dest_path):
            try:
                # Find the 'template' file inside the EXE bundle
                source_path = resPath(os.path.join("Database", filename))

                # Copy it to the writable AppData folder
                shutil.copy2(source_path, dest_path)
                print(f"Migrated {filename} to AppData")
            except Exception as e:
                print(f"Could not migrate {filename}: {e}")

    # 3. Ensure sub-files in folders also exist
    safeCreateFile(os.path.join(DB_BASE, "accounts", "accounts.json"), isList=True)


def getItems() -> list:
    return read(os.path.join(DB_BASE, "items.json"))

def updateItems(data: list) -> None:
    safeWrite(os.path.join(DB_BASE, "items.json"), data)

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
    base_path = os.path.join(DB_BASE, "summaries")

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
    safeWrite(os.path.join(DB_BASE, f"summaries/{date.year}/{date.month}/{date.day}/transactions.json"), data)

def getAccounts() -> list:
    return read(os.path.join(DB_BASE, "accounts/accounts.json"))

def getAccount(username: str) -> dict:
    return read(os.path.join(DB_BASE, f"accounts/{username}/profile.json"))

def updateAccounts(data: list) -> None:
    safeWrite(os.path.join(DB_BASE, "accounts/accounts.json"), data)

def updateAccount(username: str, data: dict) -> None:
    safeWrite(os.path.join(DB_BASE, f"accounts/{username}/profile.json"), data)

def createAccount(data: dict) -> None:
    folder = os.path.join(DB_BASE, f"accounts/{data["username"]}")
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    safeWrite(folder + "/profile.json", data)
    safeCreateFile(folder + "/shoppingCart.json", False)
    safeCreateFile(folder + "/orders.json", True)

def getOrders(username: str) -> list:
    return read(os.path.join(DB_BASE, f"accounts/{username}/orders.json"))

def updateOrders(username: str, data: list) -> None:
    safeWrite(os.path.join(DB_BASE, f"accounts/{username}/orders.json"), data)

def getCart(username: str) -> dict:
    return read(os.path.join(DB_BASE, f"accounts/{username}/shoppingCart.json"))

def updateCart(username: str, data: dict) -> None:
    safeWrite(os.path.join(DB_BASE, f"accounts/{username}/shoppingCart.json"), data)

def autoIncrement(idType: DataModels.ID) -> int:
    nextId = 0
    with open(os.path.join(DB_BASE, f"meta.json"), 'r+') as file:
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
    safeWrite(os.path.join(DB_BASE, f"meta.json"), ids)
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