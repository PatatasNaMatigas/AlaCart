import os
import json
import random
import datetime

# Configuration matching your DataModels and FileHandler
BASE_PATH = "../Database/summaries"
SELLERS = ["TechStore", "Seller123", "GamingHub"]
BUYERS = ["ae", "eli", "admin"]
ITEMS = {
    "TechStore": [
        {"id": 101, "name": "Mechanical Keyboard", "price": 2500.0},
        {"id": 105, "name": "Gaming Mouse", "price": 1200.0},
        {"id": 110, "name": "USB-C Cable", "price": 200.0}
    ],
    "Seller123": [
        {"id": 202, "name": "Espresso Beans", "price": 450.0},
        {"id": 205, "name": "Coffee Grinder", "price": 1500.0}
    ],
    "GamingHub": [
        {"id": 303, "name": "V-Bucks Pack", "price": 500.0},
        {"id": 305, "name": "Minecoins", "price": 50.0},
        {"id": 401, "name": "Robux Gift Card", "price": 250.0}
    ]
}
PAYMENT_METHODS = ["Cash", "Debit Card", "Credit Card", "GCash", "SPayLater", "Bank Transfer"]


def generateDailyTransactions(date):
    transactions = []
    # Generate 5 to 15 transactions per day for a busy year
    numTransactions = random.randint(5, 15)

    for i in range(numTransactions):
        numItems = random.randint(1, 4)
        itemsSummary = []
        totalPrice = 0

        for _ in range(numItems):
            # Pick a random seller and one of their items
            seller = random.choice(SELLERS)
            itemTemplate = random.choice(ITEMS[seller])
            quantity = random.randint(1, 3)
            subTotal = itemTemplate["price"] * quantity

            itemsSummary.append({
                "item_id": itemTemplate["id"],
                "item_name": itemTemplate["name"],
                "quantity": quantity,
                "price_at_purchase": itemTemplate["price"],
                "sub_total": subTotal,
                "owner": seller
            })
            totalPrice += subTotal

        # Ensure pay amount is sufficient
        extraPay = random.choice([0, 50, 100, 500, 1000])
        payAmount = float(totalPrice + extraPay)

        transaction = {
            "transaction_id": f"T{random.randint(100000000, 999999999)}",
            "date_time": f"{date} {random.randint(7, 21):02}:{random.randint(0, 59):02}:00",
            "buyer" : random.choice(BUYERS),
            "items_summary": itemsSummary,
            "total_price": float(totalPrice),
            "pay_amount": payAmount,
            "change": float(payAmount - totalPrice),
            "payment_method": random.choice(PAYMENT_METHODS)
        }
        transactions.append(transaction)

    return transactions


def main():
    today = datetime.date.today()
    print(f"Starting data generation for 365 days...")

    # Populate data for the last 365 days
    for i in range(365):
        currentDate = today - datetime.timedelta(days=i)

        # Create directory path: YYYY/MM/DD
        yearStr = str(currentDate.year)
        monthStr = str(currentDate.month)
        dayStr = str(currentDate.day)

        dayDir = os.path.join(BASE_PATH, yearStr, monthStr, dayStr)
        os.makedirs(dayDir, exist_ok=True)

        # Generate and save data
        data = generateDailyTransactions(currentDate)
        filePath = os.path.join(dayDir, "transactions.json")

        with open(filePath, 'w') as f:
            json.dump(data, f, indent=4)

        # Simple progress update every 30 days
        if i % 30 == 0 and i > 0:
            print(f"Generated {i} days of data...")

    print(f"\nSuccess! 1 year of transaction history created in {BASE_PATH}.")
    print("You can now test your Weekly and Monthly graphs across the entire year.")


if __name__ == "__main__":
    main()
