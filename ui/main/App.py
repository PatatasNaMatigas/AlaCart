import tkinter as tk

from dataManager.DataModels import Accounts
from ui.main.Index import Login, SignUp

from ui.customer.CustomerHome import CustomerHome
from ui.customer.Browser import Browser
from ui.customer.Transactions import Transaction
from ui.customer.CustomerProfile import CustomerProfile
from ui.customer.ShoppingCart import ShoppingCart

from ui.seller.SellerProfile import SellerProfile
from ui.seller.SellerHome import SellerHome
from ui.seller.Item import Item
from ui.seller.ItemManager import ItemManager
from ui.seller.Summaries import Summaries

from util import Utils
from util.Utils import logData

frames = {}

sellerScenes = {
    "SellerHome" : {
        "frame" : SellerHome,
        "account" : {}
    },
    "SellerProfile" : {
        "frame" : SellerProfile
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
    },
}
customerScenes = {
    "CustomerHome" : {
        "frame" : CustomerHome,
        "account" : {}
    },
    "CustomerProfile" : {
        "frame" : CustomerProfile,
    },
    "Browser" : {
        "frame" : Browser
    },
    "ShoppingCart" : {
        "frame" : ShoppingCart
    },
    "Transaction" : {
        "frame" : Transaction
    }
}

def show(name: str) -> None:
    frame = frames[name]
    frame.tkraise()
    frame.onRaise()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ala Carte")
        self.iconPhoto = tk.PhotoImage(file="../res/icon.png")
        self.iconphoto(True, self.iconPhoto)
        self.geometry("1000x600")

        Utils.initFont("koulen.ttf")
        Utils.initFont("monomaniac.ttf")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.resizable(False, False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        scenes = sellerScenes | customerScenes | {
            "Login" : {
                "frame" : Login
            },
            "SignUp" : {
                "frame" : SignUp
            }
        }

        for k, v in scenes.items():
            frame = v["frame"](container, self)
            frames[v["frame"].__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        show("Login")