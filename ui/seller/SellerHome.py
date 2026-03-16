import tkinter as tk
from datetime import datetime
from typing import Callable

from PIL import ImageTk, Image

from ui import UIUtils
from ui.main import App
from util import Utils
from util.Utils import log


class SellerHome(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#48426D")

        self.controller = controller
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#48426D",
            highlightthickness = 0
        )
        self.canvas.pack(fill="both", expand=True)

        self.descriptions = {
            "browse"    : [
                "Manage Items",
                "Add/edit/remove items\\from the store"
            ],
            "summaries" : [
                "Summary",
                "View sales, Transactions,\\Orders, and statistics"
            ],
            "signout"   : [
                "Sign-out",
                "Exit and return to login\\page"
            ],
            "profile"   : [
                "Profile",
                "modify account Settings\\and view statistics"
            ]
        }

        self.images = {}
        self.initImages()
        self.initUi()

    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["logo"] = ImageTk.PhotoImage(
            Image.open("../res/logo.png").resize((550, 130), Image.Resampling.LANCZOS)
        )
        self.images["browse"] = ImageTk.PhotoImage(
            Image.open("../res/browse.png").resize((50, 50), Image.Resampling.LANCZOS)
        )
        self.images["summaries"] = ImageTk.PhotoImage(
            Image.open("../res/summaries.png").resize((40, 40), Image.Resampling.LANCZOS)
        )
        self.images["signout"] = ImageTk.PhotoImage(
            Image.open("../res/signout.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.images["profile"] = ImageTk.PhotoImage(
            Image.open("../res/buyer_48426D.png").resize((40, 40), Image.Resampling.LANCZOS)
        )

    def initUi(self) -> None:
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )
        now = datetime.now()

        if 5 <= now.hour < 12:
            day = "Morning"
        elif 12 <= now.hour < 18:
            day = "Afternoon"
        elif 18 <= now.hour < 22:
            day = "Evening"
        else:
            day = "Night"

        username = ""
        try:
            username = App.sellerScenes["SellerHome"]["account"]["username"]
        except KeyError:
            pass

        self.canvas.create_image(
            500, 160,
            image=self.images["logo"]
        )
        self.canvas.create_text(
            500, 280,
            text=f"Good {day} {username}!",
            font=(Utils.Fonts.MONO_MANIAC.value, 30),
            fill="#F0C38E"
        )

        def onBrowseRelease():
            App.show("ItemManager")
        self.createButton(233, 340, "browse",None, onBrowseRelease)

        def onSummariesRelease():
            pass
        self.createButton(513, 340, "summaries", None, onSummariesRelease)

        def onProfileRelease():
            App.show("SellerProfile")
        self.createButton(233, 457, "profile", None, onProfileRelease)

        def onSignOutRelease():
            App.show("Login")
        self.createButton(513, 457, "signout", None, onSignOutRelease)

    def createButton(self, x: int, y: int, tag: str, onClick: Callable, onRelease: Callable) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            250, 90,
            radius=40,
            fill="#363152",
            outline="",
            tags=f"{tag}Shadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            250, 90,
            radius=40,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_image(
            x + 45, y + 45,
            image=self.images[tag]
        )
        self.canvas.create_text(
            x + 90, y + 25,
            text=self.descriptions[tag][0],
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 20),
            anchor="w"
        )
        i = 0
        for line in self.descriptions[tag][1].split("\\"):
            self.canvas.create_text(
                x + 90, y + 50 + (i * 17),
                text=line,
                fill="#48426D",
                font=(Utils.Fonts.KOULEN.value, 12),
                anchor="w",
            )
            i += 1
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            250, 90,
            radius=40,
            fill="",
            outline="",
            tags=f"{tag}Button"
        )
        def onClk(event):
            self.canvas.move(f"{tag}Shadow", -5, -5)
            if onClick:
                onClick()

        def onRls(event):
            self.canvas.move(f"{tag}Shadow", 5, 5)
            if onRelease:
                onRelease()

        self.canvas.tag_bind(f"{tag}Button", "<Button-1>", onClk)
        self.canvas.tag_bind(f"{tag}Button", "<ButtonRelease-1>", onRls)

    def onRaise(self) -> None:
        log("Raised SellerHome")

        self.canvas.delete("all")
        self.initImages()
        self.initUi()