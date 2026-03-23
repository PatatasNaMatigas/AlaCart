import json
import random
import os

from dataManager import FileHandler
from dataManager.DataModels import ID
from dataManager.FileHandler import DB_BASE

# Configuration
FILE_PATH = os.path.join(DB_BASE, "items.json")
OWNERS = ["TechStore", "Seller123", "GamingHub"]

# Item templates for each owner to make the data realistic
ITEM_TEMPLATES = {
    "TechStore": [
        {"name": "Mechanical Keyboard", "base_price": 2500, "tags": ["Tech", "Peripherals"]},
        {"name": "Gaming Mouse", "base_price": 1200, "tags": ["Tech", "Gaming"]},
        {"name": "USB-C Cable", "base_price": 200, "tags": ["Tech", "Cables"]},
        {"name": "Monitor Stand", "base_price": 1500, "tags": ["Tech", "Office"]},
        {"name": "Webcam 1080p", "base_price": 3500, "tags": ["Tech", "Streaming"]}
    ],
    "Seller123": [
        {"name": "Espresso Beans (500g)", "base_price": 450, "tags": ["Food", "Coffee"]},
        {"name": "Coffee Grinder", "base_price": 1500, "tags": ["Kitchen", "Tools"]},
        {"name": "Paper Filters", "base_price": 150, "tags": ["Kitchen", "Disposable"]},
        {"name": "Ceramic Mug", "base_price": 300, "tags": ["Home", "Dining"]},
        {"name": "Milk Frother", "base_price": 800, "tags": ["Kitchen", "Tools"]}
    ],
    "GamingHub": [
        {"name": "V-Bucks Pack (1000)", "base_price": 500, "tags": ["Digital", "Fortnite"]},
        {"name": "Robux Gift Card", "base_price": 250, "tags": ["Digital", "Roblox"]},
        {"name": "Minecoins (1720)", "base_price": 550, "tags": ["Digital", "Minecraft"]},
        {"name": "Steam Wallet (P500)", "base_price": 520, "tags": ["Digital", "Steam"]},
        {"name": "Discord Nitro (1 Mo)", "base_price": 499, "tags": ["Digital", "Social"]}
    ]
}


def generate_items():
    items_list = []

    for owner in OWNERS:
        templates = ITEM_TEMPLATES[owner]
        for template in templates:
            item = {
                "item_id": FileHandler.autoIncrement(ID.ITEM),
                "name": template["name"],
                "stock": random.randint(10, 100),
                "price": float(template["base_price"]),
                "tags": template["tags"],
                "owner": owner
            }
            items_list.append(item)

    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # Save to file
    with open(FILE_PATH, 'w') as f:
        json.dump(items_list, f, indent=4)

    print(f"Successfully generated {len(items_list)} items in {FILE_PATH}")


if __name__ == "__main__":
    generate_items()