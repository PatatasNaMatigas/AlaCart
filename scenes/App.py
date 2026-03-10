import tkinter as tk

from scenes.admin.Item import Item
from scenes.admin.Home import Home as AdminHome
from scenes.admin.ItemManager import ItemManager
from scenes.admin.Summaries import Summaries

from scenes.customer.Home import Home as CustomerHome

from util import Utils

frames = {}

adminScenes = {
    "Home" : {
        "frame" : AdminHome
    },
    "ItemManager" : {
        "frame" : ItemManager,
        "selectedItem" : {}
    },
    "Item" : {
        "frame" : Item
    },
    "Summaries" : {
        "frame" : Summaries
    }
}
customerScenes = {
    "Home" : {
        "frame" : CustomerHome
    }
}

def show(name: str) -> None:
    frame = frames[name]
    frame.tkraise()
    frame.onRaise()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        Utils.initFont("koulen.ttf")
        self.geometry("1000x600")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.resizable(False, False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        scenes = adminScenes | customerScenes

        for k, v in scenes.items():
            frame = v["frame"](container, self)
            frames[v["frame"].__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        show("ItemManager")