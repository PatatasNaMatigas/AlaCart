import tkinter as tk
from typing import Callable

from PIL import ImageTk, Image

from ui import UIUtils
from ui.main import App
from util import Utils
from util.Utils import log, logData, wtf, warn
from dataManager.DataModels import Transactions


class Transaction(tk.Frame):

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

        self.images = {}
        self.initImages()

        self.transactions = []

        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = 0

    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )
        self.canvas.create_rectangle(
            0, 515,
            1000, 520,
            fill="#363152",
            outline="",
            tags="front"
        )
        self.canvas.create_rectangle(
            0, 520,
            1000, 600,
            fill="#48426D",
            outline="",
            tags="front"
        )
        self.canvas.create_rectangle(
            0, 0,
            1000, 70,
            fill="#312C51",
            outline="",
            tags="front"
        )
        self.canvas.create_rectangle(
            0, 70,
            1000, 75,
            fill="#363152",
            outline="",
            tags="front"
        )
        self.canvas.create_text(
            500, 35,
            text="Transactions",
            font=(Utils.Fonts.KOULEN.value, 30),
            fill="#F0C38E",
            anchor='center',
            tags="front"
        )

        def done():
            App.show("CustomerProfile")

        self.createButton(
            425, 525,
            150, 50,
            "exit",
            "done",
            done,
            tags=("front", )
        )

        self.initTransactionItems()

        def scrollItems(event):
            dy = int(event.delta / 120) * 50
            newY = self.itemEntryY + dy
            if newY > self.itemEntryMaxY:
                dy = self.itemEntryMaxY - self.itemEntryY
                self.itemEntryY = self.itemEntryMaxY
            elif newY < self.itemEntryMinY:
                dy = self.itemEntryMinY - self.itemEntryY
                self.itemEntryY = self.itemEntryMinY
            else:
                self.itemEntryY = newY

            if dy != 0:
                self.canvas.move("itemEntry", 0, dy)
                self.canvas.tag_raise("front")

        self.canvas.bind_all("<MouseWheel>", scrollItems)

    def initTransactionItems(self):
        for i, transaction in enumerate(self.transactions):
            self.createItemEntry(
                350, 110 + (i * 125),
                transaction
            )

    def createItemEntry(self, x: int, y: int, transaction: dict) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            300, 100,
            radius=30,
            fill="#363152",
            outline="",
            tags=(f"{transaction["transaction_id"]}Shadow", "itemEntry")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            300, 100,
            radius=40,
            fill="#48426D",
            outline="",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 150, y + 25,
            text=f"{transaction["transaction_id"]}",
            font=(Utils.Fonts.KOULEN.value, 25),
            fill="#F0C38E",
            anchor="center",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 150, y + 60,
            text=f"Date-Time:  {transaction["date_time"]}",
            font=(Utils.Fonts.KOULEN.value, 15),
            fill="#F0C38E",
            anchor="center",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 150, y + 85,
            text=f"Total:  ₱{transaction["total_price"]:,.2f}",
            font=(Utils.Fonts.KOULEN.value, 15),
            fill="#F0C38E",
            anchor="center",
            tags="itemEntry"
        )

    def createButton(self, x: int, y: int, w: int, h: int, label: str | ImageTk.PhotoImage, tag: str, function: Callable, radius: int=30, tags: tuple=()) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            w, h,
            radius=radius,
            fill="#363152",
            outline="",
            tags=(f"{tag}Shadow",) + tags
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=radius,
            fill="#F0C38E",
            outline="",
            tags=tags
        )
        if label.__class__ == str:
            self.canvas.create_text(
                x + int(w / 2),
                y + int(h / 2),
                text=label,
                font=(Utils.Fonts.KOULEN.value, 20),
                fill="#48426D",
                tags=(tags, ) + tuple(f"{tag}Text" for tag in tags)
            )
        elif label.__class__ == ImageTk.PhotoImage:
            self.canvas.create_image(
                x + int(w / 2),
                y + int(h / 2),
                image=label,
                tags=tags
            )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=radius,
            fill="",
            outline="",
            tags=(f"{tag}Button",) + tags
        )

        def onClick(event):
            self.canvas.move(f"{tag}Shadow", -5, -5)

        def onRelease(event):
            self.canvas.move(f"{tag}Shadow", 5, 5)
            function()

        self.canvas.tag_bind(f"{tag}Button", "<Button-1>", onClick)
        self.canvas.tag_bind(f"{tag}Button", "<ButtonRelease-1>", onRelease)

    def onRaise(self):
        log("Raised Transactions")

        self.canvas.delete("all")

        self.transactions = Transactions().getUserTransactions(App.customerScenes["CustomerHome"]["account"]["username"])

        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = 0
        try:

            self.itemEntryY = 0
            self.itemEntryMaxY = 0
            self.itemEntryMinY = min(500 - (len(self.transactions) * 125), 0)
        except KeyError as e:
            pass

        self.initUi()
        self.canvas.tag_raise("front")