import tkinter as tk
from datetime import datetime
from typing import Callable

from PIL import ImageTk, Image

from util.Utils import log


class SellerProfile(tk.Frame):

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
        self.initUi()

    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["seller"] = ImageTk.PhotoImage(
            Image.open("../res/seller.png").resize((40, 40), Image.Resampling.LANCZOS)
        )

    def initUi(self) -> None:
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )

    def onRaise(self) -> None:
        log("Raised SellerProfile")

        self.canvas.delete("all")
        self.initImages()
        self.initUi()