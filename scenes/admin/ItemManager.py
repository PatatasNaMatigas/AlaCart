import tkinter as tk

from PIL import ImageTk, Image

from dataManager import DataModels as DM
from dataManager.DataModels import createItemEntry
from dataManager.SearchEngine import SearchEngine
from util.Utils import *


class ItemManager(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#303032")

        self.controller = controller
        self.widgets = Widgets()
        self.items = DM.Items()
        self.searchEngine = SearchEngine(self.items)
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#303032",
            highlightthickness = 0
        )

        self.icons = {}
        self.icons["home"] = ImageTk.PhotoImage(
            Image.open("../res/home.png").resize((40, 40), Image.LANCZOS)
        )
        self.icons["filter"] = ImageTk.PhotoImage(
            Image.open("../res/filter.png").resize((30, 30), Image.LANCZOS)
        )

        self.drawItems(self.items.getItems())
        self.drawDiv()
        self.initUX()

        self.canvas.pack(fill="both", expand=True)

    def drawDiv(self):
        self.canvas.create_rectangle(
            0, 0,
            80, 600,
            fill="#353537",
            outline=""
        )
        self.canvas.create_rectangle(
            80, 0,
            1000, 90,
            fill="#303032",
            outline=""
        )

    def initUX(self):
        # Home Button
        self.widgets.createRoundRect(
            self.canvas,
            10, 20, 60, 60,
            radius=20,
            fill="#454547",
            outline=""
        )
        self.canvas.create_image(
            40, 50,
            image=self.icons["home"],
            anchor="center"
        )
        self.widgets.createRoundRect(
            self.canvas,
            10, 20, 60, 60,
            radius=20,
            fill="",
            outline="",
            tags="homeButton"
        )
        def home(event):
            log("Home", "drawUX().home()")
        self.canvas.tag_bind("homeButton", "<Button-1>", home)

        # Search Bar
        self.initSearchBar()

        # Filter Button
        self.widgets.createRoundRect(
            self.canvas,
            900, 20,
            50, 50,
            radius=20,
            fill="#454547",
            outline=""
        )
        self.canvas.create_image(
            925, 45,
            image=self.icons["filter"],
            anchor="center"
        )
        self.widgets.createRoundRect(
            self.canvas,
            900, 20,
            50, 50,
            radius=20,
            fill="",
            outline="",
            tags="filterButton"
        )
        def filter(event):
            log("Filter", "drawUX().filter()")
        self.canvas.tag_bind("filterButton", "<Button-1>", filter)

    def initSearchBar(self):
        self.query = ""
        self.active = False
        self.widgets.createRoundRect(
            self.canvas,
            100, 20,
            790, 50,
            radius=20,
            fill="#454547",
            outline=""
        )
        self.searchText = self.canvas.create_text(
            495, 45,
            anchor="center",
            text="Search",
            font=("koulen", 25),
            fill="#818181"
        )

        self.widgets.createRoundRect(
            self.canvas,
            100, 20,
            790, 50,
            radius=20,
            fill="",
            outline="",
            tags="searchBarButton"
        )
        def onClick(event):
            self.active = True
            self.canvas.focus_set()
        self.canvas.tag_bind("searchBarButton", "<Button-1>", onClick)
        def onKeyPress(event):
            if not self.active:
                return
            if event.keysym == "BackSpace":
                self.query = self.query[:-1]
            elif event.keysym == "Escape":
                self.active = False
            elif event.keysym == "Return":
                log(f"Search for: {self.query}", "initSearchBar().onKeyPress()")
                self.canvas.delete("itemEntry")
                self.drawItems(self.searchEngine.search(self.query))
            elif len(event.char) == 1:
                self.query += event.char

            display = self.query if self.query else "Search"
            color = "#FFFFFF" if self.query else "#818181"
            self.canvas.itemconfig(self.searchText, text=display, fill=color)
        self.canvas.bind("<Key>", onKeyPress)

    def drawItems(self, items: list):
        for i in range(len(items)):
            itm = items[i]
            self.widgets.createItemEntry(
                self.canvas,
                100 + (290 * (i % 3)),
                90 + (210 * (i // 3)),
                itm["item_id"],
                itm["name"],
                itm["stock"],
                itm["price"]
            )

class Widgets:

    def createItemEntry(self, canvas: tk.Canvas, x: int, y: int, itemId:int, itemName: str, stock: int, price: float, image: str=None) -> None:
        self.createRoundRect(
            canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="#454547",
            outline="",
            tag="itemEntry"
        )
        self.createRoundRect(
            canvas,
            x, y + 130,
            270, 60,
            radius=40,
            fill="#353537",
            outline="",
            tags="itemEntry"
        )
        canvas.create_rectangle(
            x, y + 115,
            270 + x, 150 + y,
            outline="",
            fill="#353537",
            tags="itemEntry"
        )
        canvas.create_text(
            x + 10,
            y + 140,
            anchor="w",
            text=itemName,
            fill="#FFFFFF",
            font=("koulen", 20),
            tags="itemEntry"
        )
        canvas.create_text(
            x + 10,
            y + 170,
            anchor="w",
            text=f"Stock: {stock}",
            fill="#FFFFFF",
            font=("koulen", 12),
            tags="itemEntry"
        )
        canvas.create_text(
            x + 260,
            y + 170,
            anchor="e",
            text=f"Price: P{price}",
            fill="#FFFFFF",
            font=("koulen", 12),
            tags="itemEntry"
        )
        self.createRoundRect(
            canvas,
            x, y,
            270,
            190,
            radius=40,
            fill="",
            outline="",
            tag=("itemEntry", f"{itemId}")
        )

    def createRoundRect(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int=25, **kwargs):
        x2 += x1
        y2 += y1
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]

        return canvas.create_polygon(
            points,
            smooth=True,
            splinesteps=36,
            **kwargs
        )