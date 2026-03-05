import tkinter as tk
import tkinter.font as tkFont

class Home(tk.Frame):

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
        self.canvas.create_rectangle(
            0, 0,
            1000, 600,
            fill="#48426D",
            outline=""
        )