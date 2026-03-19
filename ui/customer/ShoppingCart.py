import tkinter as tk
from logging import FileHandler
from pathlib import Path
from typing import Callable

from PIL import ImageTk, Image

from dataManager import DataModels
from dataManager.Checkout import CheckoutManager
from ui import UIUtils
from ui.Codes import ReturnCode
from ui.main import App
from util import Utils
from util.Utils import log, logData, wtf, warn
from dataManager.DataModels import ShoppingCart as SC, Items, Accounts


class ShoppingCart(tk.Frame):

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

        self.icons = {}
        self.images = {}
        self.itemImages = {}
        self.initImages()

        self.shoppingCart = None
        self.cartItems = None
        self.paymentOption = 0
        self.paymentOptions = list(DataModels.Transactions.PaymentMethods)
        self.activePaymentOption = self.paymentOptions[self.paymentOption]
        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = 0
        try:
            self.shoppingCart = SC(App.customerScenes["CustomerHome"]["account"])
            self.cartItems = self.shoppingCart.getCart()

            self.itemEntryY = 0
            self.itemEntryMaxY = 0
            self.itemEntryMinY = min(500 - (len(self.cartItems) * 125), 0)
        except KeyError as e:
            pass


    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.icons["trash_9A0000"] = ImageTk.PhotoImage(
            Image.open("../res/trash_9A0000.png").resize((20, 20), Image.Resampling.LANCZOS)
        )
        self.icons["add_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/add_48426D.png").resize((20, 20), Image.Resampling.LANCZOS)
        )
        self.icons["subtract_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/subtract_48426D.png").resize((20, 4), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )
        self.canvas.create_rectangle(
            750, 0,
            1000, 600,
            fill="#48426D",
            outline=""
        )
        self.canvas.create_rectangle(
            745, 0,
            750, 600,
            fill="#363152",
            outline=""
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
            20, 0,
            text="Shopping Cart",
            font=(Utils.Fonts.KOULEN.value, 30),
            fill="#F0C38E",
            anchor='nw',
            tags="front"
        )
        self.canvas.create_text(
            875, 125,
            text="Cart details",
            font=(Utils.Fonts.KOULEN.value, 30),
            fill="#F0C38E",
            tags="front"
        )
        self.canvas.create_text(
            775, 170,
            text=f"item count: ₱{(sum(self.cartItems.values())):,.2f}",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            anchor="nw",
            tags="itemCount"
        )
        items = Items()
        total = sum(round(items.getItem(int(k.split(":")[1]))["price"] * v, 2) for k, v in self.cartItems.items())
        self.canvas.create_text(
            775, 210,
            text=f"total: ₱{total:,.2f}",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            anchor="nw",
            tags="totalPrice"
        )

        def cyclePaymentOptions():
            self.paymentOption = (self.paymentOption + 1) % len(self.paymentOptions)
            self.activePaymentOption = self.paymentOptions[self.paymentOption]
            self.canvas.itemconfig("cyclePaymentOptionsText", text=self.activePaymentOption.value)

        self.createButton(
            790, 350,
            170, 50,
            self.activePaymentOption.value,
            "cyclePaymentOptions",
            cyclePaymentOptions,
            tags=("cyclePaymentOptions", )
        )

        def placeOrder():
            checkout = CheckoutManager(
                App.customerScenes["CustomerHome"]["account"],
            )
            logData(App.customerScenes["CustomerHome"]["account"])

            code = checkout.checkout(
                App.customerScenes["CustomerHome"]["account"]["stats"]["balance"],
                self.activePaymentOption,
            )
            if code.success:
                self.canvas.delete("all")
                self.onRaise()
            UIUtils.launchErrorWindow(
                "Shopping Cart",
                code.message
            )

        self.createButton(
            790, 425,
            170, 50,
            "place order",
            "order",
            placeOrder
        )

        def done():
            App.show("Browser")

        self.createButton(
            800, 500,
            150, 50,
            "exit",
            "done",
            done
        )

        self.initCartItems()

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

    def initCartItems(self):
        items = Items()
        for i, item in enumerate(self.cartItems):
            itemId = int(item.split(":")[-1])
            self.itemImages[f"id:{itemId}"] = self.itemImages.get(f"id:{itemId}", None)

            try:
                if not self.itemImages[f"id:{itemId}"]:
                    self.itemImages[f"id:{itemId}"] = Image.open(
                        list(Path("../Database/images/").glob(f"{itemId}.*"))[0])

                    maxWidth = 70
                    maxHeight = 70

                    ratio = min(maxWidth / self.itemImages[f"id:{itemId}"].width,
                                maxHeight / self.itemImages[f"id:{itemId}"].height)

                    if ratio < 1:
                        newSize = (int(self.itemImages[f"id:{itemId}"].width * ratio),
                                   int(self.itemImages[f"id:{itemId}"].height * ratio))
                        self.itemImages[f"id:{itemId}"] = (self.itemImages[f"id:{itemId}"]
                            .resize(
                                newSize,
                                Image.Resampling.LANCZOS
                            )
                        )

                    self.itemImages[f"id:{itemId}"] = ImageTk.PhotoImage(self.itemImages[f"id:{itemId}"])
            except:
                warn(
                    f"{Utils.Colors.YELLOW.value}No image found{Utils.Colors.RED.value} that has {Utils.Colors.BLUE.value}{itemId}{Utils.Colors.RED.value} as the name!",
                    "Load Item Image"
                )
            self.createCartItemEntry(
                35, 105 + (i * 125),
                items.getItem(itemId),
                int(self.cartItems[item])
            )

    def createCartItemEntry(self, x: int, y: int, item: dict, quantity: int) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            670, 100,
            radius=30,
            fill="#363152",
            outline="",
            tags=(f"{item["item_id"]}Shadow", "itemEntry")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            670, 100,
            radius=40,
            fill="#48426D",
            outline="",
            tags="itemEntry"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            100, 100,
            radius=40,
            fill="#363152",
            outline="",
            tags="itemEntry"
        )
        self.canvas.create_rectangle(
            x + 80, y,
            x + 100, y + 100,
            fill="#363152",
            outline="",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 115, y,
            text=f"{item["name"]}",
            font=(Utils.Fonts.KOULEN.value, 25),
            fill="#F0C38E",
            anchor="nw",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 115, y + 40,
            text=f"Price: ₱{item["price"]:,.2f}",
            font=(Utils.Fonts.KOULEN.value, 15),
            fill="#F0C38E",
            anchor="nw",
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 115, y + 60,
            text=f"Subtotal: ₱{round(float(item["price"] * quantity), 2):,.2f}",
            font=(Utils.Fonts.KOULEN.value, 15),
            fill="#F0C38E",
            anchor="nw",
            tags=("itemEntry", f"{item["item_id"]}Subtotal")
        )
        self.canvas.create_image(
            x + 50, y + 50,
            image=self.itemImages[f"id:{item["item_id"]}"],
            tags="itemEntry"
        )
        self.canvas.create_text(
            x + 540, y + 70,
            text=f"{quantity}",
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 20),
            tags=("itemEntry", f"{item["item_id"]}Quantity")
        )

        def add():
            self.cartItems[f"itemId:{item["item_id"]}"] += 1
            self.shoppingCart.item(f"itemId:{item["item_id"]}", self.cartItems[f"itemId:{item["item_id"]}"])
            self.canvas.itemconfig(f"{item["item_id"]}Subtotal", text=f"Subtotal: ₱{round(float(item["price"] * self.cartItems[f"itemId:{item["item_id"]}"]), 2):,.2f}")
            self.canvas.itemconfig(f"{item["item_id"]}Quantity", text=f"{self.cartItems[f"itemId:{item["item_id"]}"]}")
            items = Items()
            total = sum(round(items.getItem(int(k.split(":")[1]))["price"] * v, 2) for k, v in self.cartItems.items())
            self.canvas.itemconfig("totalPrice", text=f"Total: ₱{total:,.2f}")
            self.canvas.itemconfig("itemCount", text=f"item count: {round(sum(self.cartItems.values()), 2)}")

        self.createButton(
            x + 480, y + 55, 30, 30,
            self.icons["add_48426D"],
            f"add{item["item_id"]}",
            add,
            20,
            tags=("itemEntry",)
        )

        def subtract():
            self.cartItems[f"itemId:{item["item_id"]}"] -= 1 if self.cartItems[f"itemId:{item["item_id"]}"] > 0 else 0
            self.shoppingCart.item(f"itemId:{item["item_id"]}", self.cartItems[f"itemId:{item["item_id"]}"])
            self.canvas.itemconfig(f"{item["item_id"]}Subtotal", text=f"Subtotal: ₱{round(float(item["price"] * self.cartItems[f"itemId:{item["item_id"]}"]), 2):,.2f}")
            self.canvas.itemconfig(f"{item["item_id"]}Quantity", text=f"{self.cartItems[f"itemId:{item["item_id"]}"]}")
            items = Items()
            total = sum(round(items.getItem(int(k.split(":")[1]))["price"] * v, 2) for k, v in self.cartItems.items())
            self.canvas.itemconfig("totalPrice", text=f"Total: ₱{total:,.2f}")
            self.canvas.itemconfig("itemCount", text=f"item count: {round(sum(self.cartItems.values()), 2)}")

        self.createButton(
            x + 570, y + 55, 30, 30,
            self.icons["subtract_48426D"],
            f"subtract{item["item_id"]}",
            subtract,
            20,
            tags=("itemEntry",)
        )

        def delete():
            self.shoppingCart.deleteItem(f"itemId:{item["item_id"]}")
            self.canvas.delete("all")
            self.onRaise()

        self.createButton(
            x + 610, y + 55, 30, 30,
            self.icons["trash_9A0000"],
            f"delete{item["item_id"]}",
            delete,
            20,
            tags=("itemEntry",)
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
        log("Raised ShoppingCart")

        self.canvas.delete("all")

        self.shoppingCart = SC(App.customerScenes["CustomerHome"]["account"])
        self.cartItems = self.shoppingCart.getCart()

        self.paymentOption = 0
        self.paymentOptions = list(DataModels.Transactions.PaymentMethods)
        self.activePaymentOption = self.paymentOptions[self.paymentOption]
        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = 0
        try:
            self.shoppingCart = SC(App.customerScenes["CustomerHome"]["account"])
            self.cartItems = self.shoppingCart.getCart()

            self.itemEntryY = 0
            self.itemEntryMaxY = 0
            self.itemEntryMinY = min(500 - (len(self.cartItems) * 125), 0)
        except KeyError as e:
            pass

        self.initUi()