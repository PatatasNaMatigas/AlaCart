# Create a program that prompts the user for their name and logs the
# entry time (you can just use a string for time) into a file named log.txt.
# The program should keep asking for names until the user types "exit".
# Ensure each entry is on a new line.
import datetime

with open("logs.txt", 'a') as logs:
    while True:
        name = input("Enter name to log (or 'exit'): ")
        if name == "exit":
            break
        logs.write(f"{name} - Logged at: {datetime.datetime.now()}\n")
    logs.close()
    print("Logging complete")