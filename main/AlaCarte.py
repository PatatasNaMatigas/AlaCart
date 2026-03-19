from dataManager import FileHandler as FH
from ui.main.App import App

FH.initDatabaseStructure()

app = App()
app.mainloop()