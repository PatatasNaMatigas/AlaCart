import tkinter as tk

from scenes.admin.ItemManager import ItemManager
from scenes.admin.Summaries import Summaries
from util import Utils


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

        self.frames = {}

        for F in (ItemManager, Summaries):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("ItemManager")

    def show(self, name):
        frame = self.frames[name]
        frame.tkraise()