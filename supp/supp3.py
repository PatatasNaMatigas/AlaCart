# Write a function backup_settings(settings_dict, filename) that takes a dictionary
# of user settings and saves it as a JSON file. Then, write a second function
# load_backup(filename) that retrieves the dictionary and prints a confirmation message.

import json

def backupSettings(settingsDict: dict, fileName: str) -> None:
    print("Backing up settings...")
    print(f"Success: Settings saved to '{fileName}'.")
    with open(fileName, "w") as file:
        json.dump(settingsDict, file, indent=4)

def loadBackup(fileName: str) -> None:
    print("Attempting to load backup ...")
    with open(fileName, "r") as file:
        data = json.load(file)
        print(f"Current Theme: {data["theme"]}")
        print(f"Current Font Size: {data["font_size"]}")
        print(f"System Status: {data["status"]}")

backupSettings(
    {
        "theme": "Dark Mode",
        "font_size": 14,
        "notifications": True,
        "status": "Online"
    },
    "config_backup.json"
)
loadBackup("config_backup.json")