import copy
import tkinter as tk
import tkinter.font as tkFont
from pathlib import Path

from PIL import ImageTk, Image

from dataManager.DataModels import Items
from dataManager.SearchEngine import SearchEngine
from util import Utils
from util.Utils import *
from ui import UIUtils
from ui.main import App

class ItemManager(tk.Frame):

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

        self.itemImage = {}
        self.icons = {}
        self.icons["add_F0C38E"] = ImageTk.PhotoImage(
            Image.open("../res/add_F0C38E.png").resize((60, 60), Image.Resampling.LANCZOS)
        )
        self.icons["home"] = ImageTk.PhotoImage(
            Image.open("../res/home.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.icons["trash_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/trash_48426D.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.icons["trash_9A0000"] = ImageTk.PhotoImage(
            Image.open("../res/trash_9A0000.png").resize((45, 45), Image.Resampling.LANCZOS)
        )
        self.icons["filter"] = ImageTk.PhotoImage(
            Image.open("../res/filter.png").resize((30, 30), Image.Resampling.LANCZOS)
        )
        self.images = {}
        self.images["blackFilter"] = ImageTk.PhotoImage(
            Image.open("../res/black_filter.png")
        )
        self.images["trashCover"] = ImageTk.PhotoImage(
            Image.open("../res/delete_cover.png").resize((270, 190), Image.Resampling.LANCZOS)
        )
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )

        self.filterIcons = [
            ImageTk.PhotoImage(
                Image.open("../res/recently_added.png").resize((30, 30), Image.Resampling.LANCZOS)
            ),
            ImageTk.PhotoImage(
                Image.open("../res/stock.png").resize((30, 30), Image.Resampling.LANCZOS)
            ),
            ImageTk.PhotoImage(
                Image.open("../res/price.png").resize((35, 35), Image.Resampling.LANCZOS)
            ),
            ImageTk.PhotoImage(
                Image.open("../res/alphabetical.png").resize((25, 25), Image.Resampling.LANCZOS)
            ),
        ]
        self.filters = [
            "recently added",
            "stock",
            "price",
            "alphabetical"
        ]
        self.sortTypeIcons = [
            ImageTk.PhotoImage(
                Image.open("../res/ascending.png").resize((30, 30), Image.Resampling.LANCZOS)
            ),
            ImageTk.PhotoImage(
                Image.open("../res/descending.png").resize((30, 30), Image.Resampling.LANCZOS)
            ),
        ]
        self.sortType = [
            "ascending",
            "descending"
        ]

        self.searchActive = False
        self.deleteActive = False
        self.filterActive = False
        self.activeFilter = 0
        self.activeSortType = 0

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"],
            tags="bg"
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
                    self.canvas.move("addButton", 0, dy)

        self.canvas.bind_all("<MouseWheel>", scrollItems)

        self.canvas.create_image(
            500, 300,
            image=self.images["blackFilter"],
            tags="filter"
        )
        UIUtils.createRoundRect(
            self.canvas,
            305, 155,
            400, 300,
            radius=40,
            fill="#363152",
            outline="",
            tags="filter",
        )
        UIUtils.createRoundRect(
            self.canvas,
            300, 150,
            400, 300,
            radius=40,
            fill="#48426D",
            outline="",
            tags="filter",
        )
        UIUtils.createRoundRect(
            self.canvas,
            300, 150,
            400, 70,
            radius=40,
            fill="#312C51",
            outline="",
            tags="filter",
        )
        self.canvas.create_rectangle(
            300, 200,
            700, 220,
            outline="",
            fill="#312C51",
            tags="filter",
        )
        self.canvas.create_rectangle(
            300, 220,
            700, 225,
            outline="",
            fill="#363152",
            tags="filter",
        )
        self.canvas.create_text(
            500, 185,
            text="Filter Items By",
            font=(Utils.Fonts.KOULEN.value, 27),
            fill="#F0C38E",
            tags="filter",
        )
        UIUtils.createRoundRect(
            self.canvas,
            440, 365,
            130, 50,
            radius=20,
            fill="#363152",
            tags=("filter", "filterExitButtonShadow"),
        )
        UIUtils.createRoundRect(
            self.canvas,
            435, 360,
            130, 50,
            radius=20,
            fill="#F0C38E",
            tags="filter",
        )
        self.canvas.create_text(
            500, 385,
            text="Done",
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 23),
            tags="filter"
        )
        UIUtils.createRoundRect(
            self.canvas,
            435, 360,
            130, 50,
            radius=20,
            fill="",
            tags=("filter", "filterExitButton"),
        )

        def onFilterExitClick(event):
            self.canvas.move("filterExitButtonShadow", -5, -5)

        def onFilterExitRelease(event):
            self.canvas.move("filterExitButtonShadow", 5, 5)
            self.filterActive = False
            self.canvas.tag_lower("filter")
            self.canvas.delete("itemEntry")
            self.initItems(Items().sort(self.activeFilter, ascending=self.activeSortType))
            self.itemEntryY = 0
            self.itemEntryMaxY = 0
            self.canvas.tag_raise("addButton")
            self.canvas.tag_raise("search")
            self.canvas.tag_raise("front")
            self.canvas.moveto("addButton", 105, 105)
            self.searchActive = False

        self.canvas.tag_bind("filterExitButton", "<Button-1>", onFilterExitClick)
        self.canvas.tag_bind("filterExitButton", "<ButtonRelease-1>", onFilterExitRelease)

        UIUtils.createRoundRect(
            self.canvas,
            380, 295,
            50, 50,
            radius=20,
            fill="#363152",
            outline="",
            tags=("filter", "filterTypeShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            375, 290,
            50, 50,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="filter"
        )
        self.canvas.create_text(
            400, 260,
            text=self.filters[self.activeFilter],
            font=(Utils.Fonts.KOULEN.value, 21),
            fill="#F0C38E",
            tags=("filter", "filterTypeText")
        )
        self.canvas.create_image(
            400, 315,
            image=self.filterIcons[self.activeFilter],
            tags=("filter", "filterTypeIcon")
        )
        UIUtils.createRoundRect(
            self.canvas,
            375, 290,
            50, 50,
            radius=20,
            fill="",
            outline="",
            tags=("filter", "filterType")
        )

        def onFilterTypeClick(event):
            self.canvas.move("filterTypeShadow", -5, -5)

        def onFilterTypeRelease(event):
            self.canvas.move("filterTypeShadow", 5, 5)
            self.activeFilter = self.activeFilter + 1 if self.activeFilter < 3 else 0
            self.canvas.itemconfig("filterTypeText", text=self.filters[self.activeFilter])
            self.canvas.itemconfig("filterTypeIcon", image=self.filterIcons[self.activeFilter])

        self.canvas.tag_bind("filterType", "<Button-1>", onFilterTypeClick)
        self.canvas.tag_bind("filterType", "<ButtonRelease-1>", onFilterTypeRelease)

        UIUtils.createRoundRect(
            self.canvas,
            580, 295,
            50, 50,
            radius=20,
            fill="#363152",
            outline="",
            tags=("filter", "sortTypeShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            575, 290,
            50, 50,
            radius=20,
            fill="#F0C38E",
            outline="",
            tags="filter"
        )
        self.canvas.create_text(
            600, 260,
            text=self.sortType[self.activeSortType],
            font=(Utils.Fonts.KOULEN.value, 21),
            fill="#F0C38E",
            tags=("filter", "sortTypeText")
        )
        self.canvas.create_image(
            600, 315,
            image=self.sortTypeIcons[self.activeSortType],
            tags=("filter", "sortTypeIcon")
        )
        UIUtils.createRoundRect(
            self.canvas,
            575, 290,
            50, 50,
            radius=20,
            fill="",
            outline="",
            tags=("filter", "sortType")
        )

        def onSortTypeClick(event):
            self.canvas.move("sortTypeShadow", -5, -5)

        def onSortTypeRelease(event):
            self.canvas.move("sortTypeShadow", 5, 5)
            self.activeSortType = self.activeSortType + 1 if self.activeSortType < 1 else 0
            self.canvas.itemconfig("sortTypeText", text=self.sortType[self.activeSortType])
            self.canvas.itemconfig("sortTypeIcon", image=self.sortTypeIcons[self.activeSortType])

        self.canvas.tag_bind("sortType", "<Button-1>", onSortTypeClick)
        self.canvas.tag_bind("sortType", "<ButtonRelease-1>", onSortTypeRelease)

        self.canvas.tag_lower("filter")

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
            tags=(f"addButton", f"addButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 100,
            270,
            190,
            radius=40,
            fill="#312C51",
            outline="",
            tags=(f"addButton")
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 230,
            270, 60,
            radius=40,
            fill="#48426D",
            outline="",
            tags=("addButton")
        )
        self.canvas.create_rectangle(
            100, 215,
            370, 250,
            outline="",
            fill="#48426D",
            tags=(f"addButton")
        )
        self.canvas.create_text(
            245, 252,
            text="Add Item",
            font=(Utils.Fonts.KOULEN.value, 23),
            fill="#F0C38E",
            anchor="center",
            tags=(f"addButton")
        )
        self.canvas.create_image(
            245, 160,
            image=self.icons["add_F0C38E"],
            anchor="center",
            tags=(f"addButton")
        )
        def addItemOnPress(event):
            self.canvas.move("addButtonShadow", -5, -5)

        def addItemOnRelease(event):
            self.canvas.move("addButtonShadow", 5, 5)
            self.searchActive = False
            App.show("Item")

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
            self.canvas.move("homeButtonShadow", -5, -5)
        def homeOnRelease(event):
            self.canvas.move("homeButtonShadow", 5, 5)
            self.searchActive = False
            App.show("SellerHome")

        self.canvas.tag_bind("homeButton", "<Button-1>", homeOnPress)
        self.canvas.tag_bind("homeButton", "<ButtonRelease-1>", homeOnRelease)

        # Delete Button
        UIUtils.createRoundRect(
            self.canvas,
            15, 100, 60, 60,
            radius=20,
            fill="#25213D",
            outline="",
            tags=("front", "trashButtonShadow")
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
            image=self.icons["trash_48426D"] if not self.deleteActive else self.icons["trash_9A0000"],
            anchor="center",
            tags=("front", "trashIcon")
        )
        UIUtils.createRoundRect(
            self.canvas,
            10, 95, 60, 60,
            radius=20,
            fill="",
            outline="",
            tags=("trashButton", "front")
        )
        def trashOnPress(event):
            self.canvas.move("trashButtonShadow", -5, -5)
        def trashOnRelease(event):
            self.canvas.move("trashButtonShadow", 5, 5)
            self.deleteActive = not self.deleteActive
            self.searchActive = False
            if self.deleteActive:
                self.canvas.itemconfig("trashIcon", image=self.icons["trash_9A0000"])
            else:
                self.canvas.itemconfig("trashIcon", image=self.icons["trash_48426D"])


        self.canvas.tag_bind("trashButton", "<Button-1>", trashOnPress)
        self.canvas.tag_bind("trashButton", "<ButtonRelease-1>", trashOnRelease)

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
            self.canvas.move("filterButtonShadow", -5, -5)
        def filterOnRelease(event):
            self.canvas.move("filterButtonShadow", 5, 5)
            self.canvas.tag_raise("filter")
            self.deleteActive = False
            self.searchActive = False
            self.filterActive = True

        self.canvas.tag_bind("filterButton", "<Button-1>", filterOnPress)
        self.canvas.tag_bind("filterButton", "<ButtonRelease-1>", filterOnRelease)

    def initSearchBar(self):
        self.query = ""
        self.searchActive = False
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
            font=(Utils.Fonts.KOULEN.value, 25),
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
                self.canvas.tag_raise("addButton")
                self.canvas.tag_raise("search")
                self.canvas.tag_raise("front")
                self.canvas.moveto("addButton", 105, 105)
                self.searchActive = False
            elif len(event.char) == 1 and event.char.isprintable():
                self.query += event.char

            display = self.query if self.query else "Search"
            self.canvas.itemconfig(self.searchText, text=display)
        self.canvas.bind("<Key>", onKeyPress)

    def initItems(self, items: list):
        for i in range(len(items)):
            itm = items[i]
            self.createItemEntry(
                100 + (290 * ((i + 1) % 3)),
                100 + (210 * ((i + 1) // 3)),
                itm["item_id"],
                itm["name"],
                itm["stock"],
                itm["price"]
            )

    def createItemEntry(self, x: int, y: int, itemId:int, itemName: str, stock: int, price: float) -> None:
        self.canvas.create_image(
            x + 135, y + 95,
            image=self.images["trashCover"],
            tags=("itemEntry", f"id_{itemId}", f"deleteCoverId_{itemId}")
        )
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

        self.itemImage[f"id:{itemId}"] = None

        try:
            self.itemImage[f"id:{itemId}"] = Image.open(list(Path("../Database/images/").glob(f"{itemId}.*"))[0])

            maxWidth = 240
            maxHeight = 100

            ratio = min(maxWidth / self.itemImage[f"id:{itemId}"].width,
                        maxHeight / self.itemImage[f"id:{itemId}"].height)

            if ratio < 1:
                newSize = (int(self.itemImage[f"id:{itemId}"].width * ratio),
                           int(self.itemImage[f"id:{itemId}"].height * ratio))
                self.itemImage[f"id:{itemId}"] = (self.itemImage[f"id:{itemId}"]
                                                  .resize(
                                                        newSize,
                                                        Image.Resampling.LANCZOS
                                                  )
                )

            self.itemImage[f"id:{itemId}"] = ImageTk.PhotoImage(self.itemImage[f"id:{itemId}"])

            self.canvas.create_image(
                x + 135, y + 57,
                image=self.itemImage[f"id:{itemId}"],
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
            if not self.deleteActive:
                App.sellerScenes["ItemManager"]["selectedItem"] = copy.deepcopy(self.items.getItem(int(itemId)))
                App.show("Item")
            else:
                self.items = Items()
                self.items.deleteItem(itemId)
                self.canvas.delete("all")
                self.deleteActive = True
                self.initUi()

        def onMouseHover(event, itemId):
            if self.deleteActive:
                self.canvas.tag_raise(f"deleteCoverId_{itemId}")
                self.canvas.tag_raise("search")
                self.canvas.tag_raise("front")

        def onMouseHoverLeave(event, itemId):
            if self.deleteActive:
                self.canvas.tag_lower(f"deleteCoverId_{itemId}")

        self.canvas.tag_bind(f"id_{itemId}", "<Button-1>", lambda e, i=itemId: onClick(e, i))
        self.canvas.tag_bind(f"id_{itemId}", "<ButtonRelease-1>", lambda e, i=itemId: onRelease(e, i))
        self.canvas.tag_bind(f"id_{itemId}", "<Enter>", lambda e, i=itemId: onMouseHover(e, i))
        self.canvas.tag_bind(f"id_{itemId}", "<Leave>", lambda e, i=itemId: onMouseHoverLeave(e, i))

    def onRaise(self):
        log("Raised ItemManager")

        self.items = Items()
        self.canvas.delete("all")
        self.deleteActive = False
        self.searchActive = False
        self.filterActive = False
        self.activeFilter = 0
        self.activeSortType = 0
        self.initUi()
