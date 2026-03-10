# Create a CSV file named inventory.csv with columns: Item, Quantity, Price.
# Write a script that reads this file and prints only the items where the
# Quantity is less than 5 (Low Stock Alert).
import csv

with open("inventory.csv", 'r') as inventory:
    lowStock = []
    data = csv.reader(inventory)
    for line in data:
        if int(line[1]) < 5:
            lowStock.append(line)
    inventory.close()

    if len(lowStock) > 0:
        print("--- LOW STOCK ALERT ---")
        for data in lowStock:
            print(f"Item: {data[0]} | Current Stock: {data[1]}")
        print("--------------------------------------")
        print(f"Total items requiring restock: {len(lowStock)}")