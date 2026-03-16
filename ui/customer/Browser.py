import copy
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path
from typing import Callable

from PIL import ImageTk, Image

from dataManager import DataModels as DM
from dataManager.DataModels import Items, ShoppingCart
from dataManager.SearchEngine import SearchEngine
from util import Utils
from util.Utils import *
from ui import UIUtils
from ui.main import App

class Browser(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#48426D")
        self.controller = controller

        self.items = Items()
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#48426D",
            highlightthickness = 0
        )
        self.canvas.pack(fill="both", expand=True)

        self.itemImages = {}
        self.coverItemImages = {}
        self.icons = {}
        self.icons["add_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/add_48426D.png").resize((35, 35), Image.Resampling.LANCZOS)
        )
        self.icons["subtract_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/subtract_48426D.png").resize((35, 7), Image.Resampling.LANCZOS)
        )
        self.icons["home"] = ImageTk.PhotoImage(
            Image.open("../res/home.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.icons["shoppingCart_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/shopping_cart_48426D.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.images = {}
        self.images["blackFilter"] = ImageTk.PhotoImage(
            Image.open("../res/black_filter.png")
        )
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )

        self.searchActive = False
        self.filterActive = False

        self.shoppingCart = None
        self.cartItems = None
        try:
            self.shoppingCart = ShoppingCart(App.customerScenes["CustomerHome"]["account"])
            self.cartItems = self.shoppingCart.getCart()
        except KeyError as e:
            pass
        self.activeItem = None

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"],
            tags="bg"
        )

        self.itemList = self.items.getItems()
        self.initItems(self.itemList)
        self.initDiv()
        self.initUX()
        self.initItemDetails()

        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = min(500 - ((len(self.itemList) + 2) // 3 * 210) - 90, 0)

        def scrollItems(event):
            if not self.filterActive:
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

        self.canvas.bind_all("<MouseWheel>", scrollItems)

    def initDiv(self):
        self.canvas.create_rectangle(
            80, 0,
            1000, 95,
            fill="#363152",
            outline="",
            tags="search"
        )
        self.canvas.create_rectangle(
            80, 0,
            1000, 90,
            fill="#48426D",
            outline="",
            tags="search"
        )
        self.canvas.create_rectangle(
            0, 0,
            85, 600,
            fill="#25213D",
            outline="",
            tags="front"
        )
        self.canvas.create_rectangle(
            0, 0,
            80, 600,
            fill="#312C51",
            outline="",
            tags="front"
        )

    def initUX(self):
        # Home Button
        UIUtils.createRoundRect(
            self.canvas,
            15, 25, 60, 60,
            radius=20,
            fill="#25213D",
            outline="",
            tags=("front", "homeButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            10, 20, 60, 60,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="front"
        )
        self.canvas.create_image(
            40, 50,
            image=self.icons["home"],
            anchor="center",
            tags="front"
        )
        UIUtils.createRoundRect(
            self.canvas,
            10, 20, 60, 60,
            radius=20,
            fill="",
            outline="",
            tags=("homeButton", "front")
        )
        def homeOnPress(event):
            self.canvas.move("homeButtonShadow", -5, -5)
        def homeOnRelease(event):
            self.canvas.move("homeButtonShadow", 5, 5)
            self.searchActive = False
            App.show("CustomerHome")

        self.canvas.tag_bind("homeButton", "<Button-1>", homeOnPress)
        self.canvas.tag_bind("homeButton", "<ButtonRelease-1>", homeOnRelease)

        # Shopping Cart Button
        UIUtils.createRoundRect(
            self.canvas,
            15, 100, 60, 60,
            radius=20,
            fill="#25213D",
            outline="",
            tags=("front", "cartButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            10, 95, 60, 60,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="front"
        )
        self.canvas.create_image(
            40, 125,
            image=self.icons["shoppingCart_48426D"],
            anchor="center",
            tags=("front", "cartIcon")
        )
        UIUtils.createRoundRect(
            self.canvas,
            10, 95, 60, 60,
            radius=20,
            fill="",
            outline="",
            tags=("cartButton", "front")
        )
        def cartOnPress(event):
            self.canvas.move("cartButtonShadow", -5, -5)
        def cartOnRelease(event):
            self.canvas.move("cartButtonShadow", 5, 5)
            self.searchActive = False
            App.show("ShoppingCart")

        self.canvas.tag_bind("cartButton", "<Button-1>", cartOnPress)
        self.canvas.tag_bind("cartButton", "<ButtonRelease-1>", cartOnRelease)

        # Search Bar
        self.initSearchBar()

    def initSearchBar(self):
        self.query = ""
        self.searchActive = False
        UIUtils.createRoundRect(
            self.canvas,
            105, 25,
            850, 50,
            radius=20,
            fill="#363152",
            outline="",
            tags=("search", "searchButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 20,
            850, 50,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="search"
        )
        self.searchText = self.canvas.create_text(
            495, 45,
            anchor="center",
            text="Search",
            font=(Utils.Fonts.KOULEN.value, 25),
            fill="#48426D",
            tags="search"
        )

        UIUtils.createRoundRect(
            self.canvas,
            100, 20,
            850, 50,
            radius=20,
            fill="",
            outline="",
            tags=("searchBarButton", "search")
        )
        def onClick(event):
            self.searchActive = True
            self.canvas.move("searchButtonShadow", -5, -5)
        def onRelease(event):
            self.canvas.move("searchButtonShadow", 5, 5)
            self.canvas.focus_set()

        self.canvas.tag_bind("searchBarButton", "<Button-1>", onClick)
        self.canvas.tag_bind("searchBarButton", "<ButtonRelease-1>", onRelease)
        def onKeyPress(event):
            if not self.searchActive:
                return
            if event.keysym == "BackSpace":
                self.query = self.query[:-1]
            elif event.keysym == "Escape":
                self.searchActive = False
            elif event.keysym == "Return":
                items = SearchEngine(self.items).search(self.query)
                self.canvas.delete("itemEntry")
                self.initItems(items if self.query else self.items.getItems())
                self.itemEntryY = 0
                self.itemEntryMaxY = 0
                self.canvas.tag_raise("search")
                self.canvas.tag_raise("front")
                self.searchActive = False
            elif len(event.char) == 1 and event.char.isprintable():
                self.query += event.char

            display = self.query if self.query else "Search"
            self.canvas.itemconfig(self.searchText, text=display)
        self.canvas.bind("<Key>", onKeyPress)

    def initItemDetails(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["blackFilter"],
            tags="itemDetails"
        )
        self.canvas.lower("blackBg")
        UIUtils.createRoundRect(
            self.canvas,
            305, 55,
            400, 500,
            radius=40,
            fill="#363152",
            outline="",
            tags="itemDetails"
        )
        UIUtils.createRoundRect(
            self.canvas,
            300, 50,
            400, 500,
            radius=40,
            fill="#312C51",
            outline="",
            tags="itemDetails"
        )
        self.canvas.create_rectangle(
            300, 250,
            700, 300,
            fill="#48426D",
            outline="",
            tags="itemDetails"
        )
        UIUtils.createRoundRect(
            self.canvas,
            300, 250,
            400, 300,
            radius=40,
            fill="#48426D",
            outline="",
            tags="itemDetails"
        )
        self.canvas.create_image(
            500, 150,
            tags=("itemDetails", "selectedItemImage"),
        )
        self.canvas.create_text(
            500, 300,
            text="Item name",
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 30),
            tags=("itemDetails", "selectedItemName")
        )
        self.canvas.create_text(
            500, 350,
            fill="#F0C38E",
            text="Item price",
            font=(Utils.Fonts.KOULEN.value, 20),
            tags=("itemDetails", "selectedItemPrice")
        )
        self.canvas.create_text(
            500, 410,
            fill="#F0C38E",
            text="0",
            font=(Utils.Fonts.KOULEN.value, 30),
            tags=("itemDetails", "selectedItemQuantity")
        )

        def decrement():
            if self.activeItem:
                self.cartItems[f"{self.activeItem}"] -= 1 if self.cartItems[f"{self.activeItem}"] > 0 else 0
                item = Items().getItem(int(self.activeItem.split(":")[-1]))
                self.canvas.itemconfig("selectedItemQuantity", text=f"{self.cartItems[f"{self.activeItem}"]}")
                self.canvas.itemconfig(f"selectedItemPrice", text=f"Price: {item["price"]} | subtotal: P{round(item["price"] * self.cartItems[self.activeItem], 2)}")

        self.createButton(
            390, 385,
            50, 50,
            self.icons["subtract_48426D"],
            "decrement",
            decrement
        )

        def increment():
            if self.activeItem:
                self.cartItems[f"{self.activeItem}"] += 1
                item = Items().getItem(int(self.activeItem.split(":")[-1]))
                self.canvas.itemconfig("selectedItemQuantity", text=f"{self.cartItems[f"{self.activeItem}"]}")
                self.canvas.itemconfig(f"selectedItemPrice", text=f"Price: {item["price"]} | subtotal: P{round(item["price"] * self.cartItems[self.activeItem], 2)}")

        self.createButton(
            560, 385,
            50, 50,
            self.icons["add_48426D"],
            "increment",
            increment
        )

        def done():
            self.canvas.tag_lower("itemDetails")
            if self.cartItems.get(f"{self.activeItem}", 0) <= 0:
                self.cartItems.pop(self.activeItem)

            self.shoppingCart.item(self.activeItem, self.cartItems[f"{self.activeItem}"])
            self.activeItem = None

        self.createButton(
            435, 460,
            130, 50,
            "done",
            "done",
            done
        )

        self.canvas.tag_lower("itemDetails")

    def createButton(self, x: int, y: int, w: int, h: int, label: str | ImageTk.PhotoImage, tag: str, function: Callable):
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            w, h,
            radius=30,
            fill="#363152",
            outline="",
            tags=(f"{tag}Shadow", "itemDetails")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=30,
            fill="#F0C38E",
            outline="",
            tags="itemDetails"
        )
        if label.__class__ == str:
            self.canvas.create_text(
                x + int(w / 2),
                y + int(h / 2),
                text=label,
                font=(Utils.Fonts.KOULEN.value, 25),
                fill="#48426D",
                tags="itemDetails"
            )
        elif label.__class__ == ImageTk.PhotoImage:
            self.canvas.create_image(
                x + int(w / 2),
                y + int(h / 2),
                image=label,
                tags="itemDetails"
            )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=30,
            fill="",
            outline="",
            tags=(f"{tag}Button", "itemDetails")
        )

        def onClick(event):
            self.canvas.move(f"{tag}Shadow", -5, -5)

        def onRelease(event):
            self.canvas.move(f"{tag}Shadow", 5, 5)
            function()

        self.canvas.tag_bind(f"{tag}Button", "<Button-1>", onClick)
        self.canvas.tag_bind(f"{tag}Button", "<ButtonRelease-1>", onRelease)

    def launchItemDetails(self, itemId: int):
        self.canvas.tag_raise("itemDetails")
        item = self.items.getItem(itemId)
        self.canvas.itemconfig(f"selectedItemName", text=f"{item["name"]}")
        self.canvas.itemconfig(f"selectedItemPrice", text=f"Price: {item["price"]} | subtotal: P{round(item["price"] * self.cartItems[self.activeItem], 2)}")
        self.canvas.itemconfig("selectedItemQuantity", text=f"{self.cartItems[f"{self.activeItem}"]}")

        self.coverItemImages[f"id:{itemId}"] = self.coverItemImages.get(f"id:{itemId}", None)

        try:
            if not self.coverItemImages[f"id:{itemId}"]:
                self.coverItemImages[f"id:{itemId}"] = Image.open(list(Path("../Database/images/").glob(f"{itemId}.*"))[0])

                maxWidth = 350
                maxHeight = 150

                ratio = min(maxWidth / self.coverItemImages[f"id:{itemId}"].width,
                            maxHeight / self.coverItemImages[f"id:{itemId}"].height)

                if ratio < 1:
                    newSize = (int(self.coverItemImages[f"id:{itemId}"].width * ratio),
                               int(self.coverItemImages[f"id:{itemId}"].height * ratio))
                    self.coverItemImages[f"id:{itemId}"] = (self.coverItemImages[f"id:{itemId}"]
                    .resize(
                        newSize,
                        Image.Resampling.LANCZOS
                    )
                    )

                self.coverItemImages[f"id:{itemId}"] = ImageTk.PhotoImage(self.coverItemImages[f"id:{itemId}"])
        except:
            wtf(
                f"{Utils.Colors.YELLOW.value}No image found{Utils.Colors.RED.value} that has {Utils.Colors.BLUE.value}{itemId}{Utils.Colors.RED.value} as the name!",
                "Load Item Image"
            )

        self.canvas.itemconfig("selectedItemImage", image=self.coverItemImages[f"id:{itemId}"])

    def initItems(self, items: list):
        for i in range(len(items)):
            itm = items[i]
            self.createItemEntry(
                100 + (290 * (i % 3)),
                100 + (210 * (i // 3)),
                itm["item_id"],
                itm["name"],
                itm["stock"],
                itm["price"]
            )

    def createItemEntry(self, x: int, y: int, itemId:int, itemName: str, stock: int, price: float) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            270,
            190,
            radius=40,
            fill="#363152",
            outline="",
            tags=("itemEntry", f"id_{itemId}", f"itemEntry{itemId}ButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="#312C51",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )

        self.itemImages[f"id:{itemId}"] = None

        try:
            self.itemImages[f"id:{itemId}"] = Image.open(list(Path("../Database/images/").glob(f"{itemId}.*"))[0])

            maxWidth = 240
            maxHeight = 100

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

            self.canvas.create_image(
                x + 135, y + 57,
                image=self.itemImages[f"id:{itemId}"],
                tags=("itemEntry", f"id_{itemId}")
            )
        except:
            wtf(
                f"{Utils.Colors.YELLOW.value}No image found{Utils.Colors.RED.value} that has {Utils.Colors.BLUE.value}{itemId}{Utils.Colors.RED.value} as the name!",
                "Load Item Image"
            )

        UIUtils.createRoundRect(
            self.canvas,
            x, y + 130,
            270, 60,
            radius=40,
            fill="#48426D",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )
        self.canvas.create_rectangle(
            x, y + 115,
            270 + x, 150 + y,
            outline="",
            fill="#48426D",
            tags=("itemEntry", f"id_{itemId}")
        )
        koulen = tkFont.Font(family=Utils.Fonts.KOULEN.value, size=20)
        width = koulen.measure(itemName)
        while koulen.measure(itemName + "...") > 250:
            itemName = itemName[:-1]
        if width > 250:
            itemName += "..."
        self.canvas.create_text(
            x + 10,
            y + 140,
            anchor="w",
            text=itemName,
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 20),
            tags=("itemEntry", f"id_{itemId}")
        )
        self.canvas.create_text(
            x + 10,
            y + 170,
            anchor="w",
            text=f"Stock: {stock}",
            fill="#F0C38E" if stock > 5 else "#990000",
            font=(Utils.Fonts.KOULEN.value, 12),
            tags=("itemEntry", f"id_{itemId}")
        )
        self.canvas.create_text(
            x + 260,
            y + 170,
            anchor="e",
            text=f"Price: P{price}",
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 12),
            tags=("itemEntry", f"id_{itemId}")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )

        def onClick(event, itemId):
            self.canvas.move(f"itemEntry{itemId}ButtonShadow", -5, -5)

        def onRelease(event, itemId):
            self.canvas.move(f"itemEntry{itemId}ButtonShadow", 5, 5)
            self.searchActive = False
            self.activeItem = f"itemId:{itemId}"
            self.cartItems[self.activeItem] = self.cartItems.get(self.activeItem, 0)
            self.launchItemDetails(itemId)

        self.canvas.tag_bind(f"id_{itemId}", "<Button-1>", lambda e, i=itemId: onClick(e, i))
        self.canvas.tag_bind(f"id_{itemId}", "<ButtonRelease-1>", lambda e, i=itemId: onRelease(e, i))

    def onRaise(self):
        log("Raised Browser")

        self.shoppingCart = ShoppingCart(App.customerScenes["CustomerHome"]["account"])
        self.cartItems = self.shoppingCart.getCart()

        self.items = Items()
        self.canvas.delete("all")
        self.searchActive = False
        self.initUi()