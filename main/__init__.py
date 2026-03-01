from dataManager import FileHandler as FH
from dataManager.DataModels import Items
from scenes.App import App

FH.initDatabaseStructure()

items = Items()

app = App()
app.mainloop()