import tkinter as tk
import tkinter.font as tkFont

from PIL import ImageTk, Image

from dataManager import DataModels as DM
from dataManager.SearchEngine import SearchEngine
from util.Utils import *
from scenes import App, UIUtils


class ItemManager(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#48426D")

        self.controller = controller
        self.items = DM.Items()
        self.searchEngine = SearchEngine(self.items)
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#48426D",
            highlightthickness = 0
        )
        self.canvas.create_rectangle(
            0, 0,
            1000, 600,
            fill="#48426D",
            outline=""
        )

        self.icons = {}
        self.icons["add"] = ImageTk.PhotoImage(
            Image.open("../res/add.png").resize((60, 60), Image.Resampling.LANCZOS)
        )
        self.icons["home"] = ImageTk.PhotoImage(
            Image.open("../res/home.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.icons["filter"] = ImageTk.PhotoImage(
            Image.open("../res/filter.png").resize((30, 30), Image.Resampling.LANCZOS)
        )
        self.images = {}
        self.images["blackFilter"] = ImageTk.PhotoImage(
            Image.open("../res/black_filter.png")
        )
        self.itemList = self.items.getItems()
        self.initItems(self.itemList)
        self.initAddButton()
        self.initDiv()
        self.initUX()

        self.itemEntryY = 0
        self.itemEntryMaxY = 0
        self.itemEntryMinY = min(325 - ((len(self.itemList) + 2) // 3 * 210) - 90, 0)

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

        self.canvas.bind_all("<MouseWheel>", scrollItems)

        self.canvas.create_image(
            500, 300,
            image=self.images["blackFilter"],
            tags="blackFilter"
        )
        self.canvas.tag_lower("blackFilter")

        self.canvas.pack(fill="both", expand=True)

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

    def initAddButton(self):
        UIUtils.createRoundRect(
            self.canvas,
            105, 105,
            270,
            190,
            radius=40,
            fill="#363152",
            outline="",
            tags=("itemEntry", f"addButton", f"addButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 100,
            270,
            190,
            radius=40,
            fill="#312C51",
            outline="",
            tags=("itemEntry", f"addButton")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 230,
            270, 60,
            radius=40,
            fill="#48426D",
            outline="",
            tags=("itemEntry", "addButton")
        )
        self.canvas.create_rectangle(
            100, 215,
            370, 250,
            outline="",
            fill="#48426D",
            tags=("itemEntry", f"addButton")
        )
        self.canvas.create_text(
            245, 252,
            text="Add Item",
            font=("koulen", 23),
            fill="#F0C38E",
            anchor="center",
            tags=("itemEntry", f"addButton")
        )
        self.canvas.create_image(
            245, 160,
            image=self.icons["add"],
            anchor="center",
            tags=("itemEntry", f"addButton")
        )
        def addItemOnPress(event):
            log("Add Item", "initUX().addItem()")
            self.canvas.move("addButtonShadow", -5, -5)

        def addItemOnRelease(event):
            self.canvas.move("addButtonShadow", 5, 5)
            App.show("AddItem")

        self.canvas.tag_bind("addButton", "<Button-1>", addItemOnPress)
        self.canvas.tag_bind("addButton", "<ButtonRelease-1>", addItemOnRelease)

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
            log("Home", "initUX().home()")
            self.canvas.move("homeButtonShadow", -5, -5)
        def homeOnRelease(event):
            self.canvas.move("homeButtonShadow", 5, 5)

        self.canvas.tag_bind("homeButton", "<Button-1>", homeOnPress)
        self.canvas.tag_bind("homeButton", "<ButtonRelease-1>", homeOnRelease)

        # Search Bar
        self.initSearchBar()

        # Filter Button
        UIUtils.createRoundRect(
            self.canvas,
            905, 25,
            50, 50,
            radius=20,
            fill="#363152",
            outline="",
            tags=("filterButtonShadow", "front")
        )
        UIUtils.createRoundRect(
            self.canvas,
            900, 20,
            50, 50,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="front"
        )
        self.canvas.create_image(
            925, 45,
            image=self.icons["filter"],
            anchor="center",
            tags="front"
        )
        UIUtils.createRoundRect(
            self.canvas,
            900, 20,
            50, 50,
            radius=20,
            fill="",
            outline="",
            tags=("filterButton", "front")
        )
        def filterOnPress(event):
            log("Filter", "initUX().filter()")
            self.canvas.move("filterButtonShadow", -5, -5)
            self.canvas.tag_raise("blackFilter")
        def filterOnRelease(event):
            self.canvas.move("filterButtonShadow", 5, 5)

        self.canvas.tag_bind("filterButton", "<Button-1>", filterOnPress)
        self.canvas.tag_bind("filterButton", "<ButtonRelease-1>", filterOnRelease)

    def initSearchBar(self):
        self.query = ""
        self.active = False
        UIUtils.createRoundRect(
            self.canvas,
            105, 25,
            790, 50,
            radius=20,
            fill="#363152",
            outline="",
            tags=("search", "searchButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 20,
            790, 50,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="search"
        )
        self.searchText = self.canvas.create_text(
            495, 45,
            anchor="center",
            text="Search",
            font=("koulen", 25),
            fill="#48426D",
            tags="search"
        )

        UIUtils.createRoundRect(
            self.canvas,
            100, 20,
            790, 50,
            radius=20,
            fill="",
            outline="",
            tags=("searchBarButton", "search")
        )
        def onClick(event):
            self.active = True
            self.canvas.focus_set()
            self.canvas.move("searchButtonShadow", -5, -5)
        def onRelease(event):
            self.canvas.move("searchButtonShadow", 5, 5)

        self.canvas.tag_bind("searchBarButton", "<Button-1>", onClick)
        self.canvas.tag_bind("searchBarButton", "<ButtonRelease-1>", onRelease)
        def onKeyPress(event):
            if not self.active:
                return
            if event.keysym == "BackSpace":
                self.query = self.query[:-1]
            elif event.keysym == "Escape":
                self.active = False
            elif event.keysym == "Return":
                log(f"Search for: {self.query}", "initSearchBar().onKeyPress()")
                items = self.searchEngine.search(self.query)
                self.canvas.delete("itemEntry")
                self.initItems(items)
                self.itemEntryY = 0
                self.itemEntryMaxY = 0
                self.canvas.tag_raise("search")
                self.canvas.tag_raise("front")
                self.active = False
            elif len(event.char) == 1 and event.char.isprintable():
                self.query += event.char

            display = self.query if self.query else "Search"
            self.canvas.itemconfig(self.searchText, text=display)
        self.canvas.bind("<Key>", onKeyPress)

    def initItems(self, items: list):
        for i in range(len(items)):
            itm = items[i]
            self.createItemEntry(
                self.canvas,
                100 + (290 * ((i + 1) % 3)),
                100 + (210 * ((i + 1) // 3)),
                itm["item_id"],
                itm["name"],
                itm["stock"],
                itm["price"]
            )

    def createItemEntry(self, canvas: tk.Canvas, x: int, y: int, itemId:int, itemName: str, stock: int, price: float, image: str=None) -> None:
        UIUtils.createRoundRect(
            canvas,
            x + 5, y + 5,
            270,
            190,
            radius=40,
            fill="#363152",
            outline="",
            tags=("itemEntry", f"id_{itemId}", f"itemEntry{itemId}ButtonShadow")
        )
        UIUtils.createRoundRect(
            canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="#312C51",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )
        UIUtils.createRoundRect(
            canvas,
            x, y + 130,
            270, 60,
            radius=40,
            fill="#48426D",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )
        canvas.create_rectangle(
            x, y + 115,
            270 + x, 150 + y,
            outline="",
            fill="#48426D",
            tags=("itemEntry", f"id_{itemId}")
        )
        koulen = tkFont.Font(family="koulen", size=20)
        while koulen.measure(itemName + "...") > 250:
            itemName = itemName[:-1]
        itemName += "..."
        canvas.create_text(
            x + 10,
            y + 140,
            anchor="w",
            text=itemName,
            fill="#F0C38E",
            font=("koulen", 20),
            tags=("itemEntry", f"id_{itemId}")
        )
        canvas.create_text(
            x + 10,
            y + 170,
            anchor="w",
            text=f"Stock: {stock}",
            fill="#F0C38E",
            font=("koulen", 12),
            tags=("itemEntry", f"id_{itemId}")
        )
        canvas.create_text(
            x + 260,
            y + 170,
            anchor="e",
            text=f"Price: P{price}",
            fill="#F0C38E",
            font=("koulen", 12),
            tags=("itemEntry", f"id_{itemId}")
        )
        UIUtils.createRoundRect(
            canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="",
            outline="",
            tags=("itemEntry", f"id_{itemId}")
        )

        def getItem(event):
            self.canvas.move(f"itemEntry{itemId}ButtonShadow", -5, -5)
            current_item_clicked = canvas.find_closest(event.x, event.y)
            tags = canvas.gettags(current_item_clicked)
            actual_id = None
            for tag in tags:
                if tag.startswith("id_"):
                    actual_id = tag.split("_")[1]
                    break

            if actual_id:
                log(f"Clicked on item ID: {actual_id}")
                logData(self.items.getItem(int(actual_id)))

        def onRelease(event):
            self.canvas.move(f"itemEntry{itemId}ButtonShadow", 5, 5)

        canvas.tag_bind(f"id_{itemId}", "<Button-1>", getItem)
        canvas.tag_bind(f"id_{itemId}", "<ButtonRelease-1>", onRelease)