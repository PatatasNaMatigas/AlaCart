from dataManager import FileHandler as FH
from dataManager.DataModels import Items, Accounts
from scenes.App import App

FH.initDatabaseStructure()

Accounts().createAccount("admin", "admin", Accounts.Role.OWNER)

app = App()
app.mainloop()