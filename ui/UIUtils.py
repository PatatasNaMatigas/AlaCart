import tkinter as tk

from PIL import Image, ImageTk

import tkinter.font as tkFont

from ui.Codes import ReturnCode, ThreatLevel
from util import Utils


def createRoundRect(canvas: tk.Canvas, x: int, y: int, w: int, h: int, radius: int = 25, **kwargs):
    w += x
    h += y
    points = [
        x + radius, y,
        w - radius, y,
        w, y,
        w, y + radius,
        w, h - radius,
        w, h,
        w - radius, h,
        x + radius, h,
        x, h,
        x, h - radius,
        x, y + radius,
        x, y,
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=36,
        **kwargs
    )

def launchErrorWindow(title: str, message: str) -> None:
    window = Window(400, 300, title, message, ErrorWindow)
    window.mainloop()

class ErrorWindow(tk.Frame):

    def __init__(self, parent, controller, width: int, height: int, message: str, done):
        super().__init__(parent)
        self.controller = controller

        self.width = width
        self.height = height
        self.message = message
        self.done = done

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg="#312C51",
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.images = {}
        self.initImages()

        self.initUi()

    def initImages(self):
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((800, 400), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.canvas.create_image(
            self.width / 2,
            self.height / 2,
            image=self.images["bg"]
        )
        createRoundRect(
            self.canvas,
            44, 44,
            320, 220,
            radius=40,
            fill="#3B3558",
            outline=""
        )
        createRoundRect(
            self.canvas,
            40, 40,
            320, 220,
            radius=40,
            fill="#48426D",
            outline=""
        )

        font = (Utils.Fonts.KOULEN.value, 17)
        koulen = tkFont.Font(family=font[0], size=font[1])

        words = self.message.split()
        lines = []
        currentLine = ""

        for word in words:
            temp = f"{currentLine} {word}".strip()

            if koulen.measure(temp) <= 280:
                currentLine = temp
            else:
                lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        for i, line in enumerate(lines):
            self.canvas.create_text(
                200, 80 + (i * 36),
                text=line,
                font=font,
                fill="#F0C38E",
                anchor="center"
            )

        createRoundRect(
            self.canvas,
            165, 195,
            80, 40,
            radius=30,
            fill="#363152",
            outline="",
            tags="doneButtonShadow"
        )
        createRoundRect(
            self.canvas,
            160, 190,
            80, 40,
            radius=30,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_text(
            200, 210,
            text="done",
            fill="#48426D",
            font=font
        )
        createRoundRect(
            self.canvas,
            160, 190,
            80, 40,
            radius=30,
            fill="",
            outline="",
            tags="doneButton"
        )

        def onDoneClick(event):
            self.canvas.move("doneButtonShadow", -5, -5)
        def onDoneRelease(event):
            self.canvas.move("doneButtonShadow", 5, 5)
            self.canvas.tag_unbind("doneButton", "<Button-1>")
            self.canvas.tag_unbind("doneButton", "<ButtonRelease-1>")
            self.after(10, self.done)

        self.canvas.tag_bind("doneButton", "<Button-1>", onDoneClick)
        self.canvas.tag_bind("doneButton", "<ButtonRelease-1>", onDoneRelease)

class Window(tk.Toplevel):

    def __init__(self, width: int, height: int, title: str, message: str, frame: type[tk.Frame]):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")

        Utils.initFont("koulen.ttf")
        Utils.initFont("monomaniac.ttf")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.resizable(False, False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frm = frame(container, self, width, height, message, self.done)
        frm.grid(row=0, column=0, sticky="nsew")


    def done(self):
        self.destroy()