from dataManager import FileHandler as FH
from dataManager.DataModels import Accounts
from ui import UIUtils
from ui.Codes import ReturnCode, ThreatLevel
from ui.main.App import App

FH.initDatabaseStructure()

app = App()
app.mainloop()