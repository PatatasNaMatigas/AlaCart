import tkinter as tk

from PIL import ImageTk, Image

from dataManager.DataModels import Accounts
from scenes import UIUtils


class Index(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#312C51")
        self.controller = controller

        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#312C51",
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Key>", self.onKeyPress)

        self.images = {}
        self.initImages()

        self.focusedField = None
        self.username = ["", "Enter username", "username"]
        self.password = ["", "Enter password", "password"]

        self.initUi()

    def initImages(self):
        self.images["logo"] = ImageTk.PhotoImage(
            Image.open("../res/logo.png").resize((250, 60), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.initLoginForm()

    def initLoginForm(self):
        UIUtils.createRoundRect(
            self.canvas,
            305, 55,
            400, 500,
            radius=70,
            fill="#25213D",
            outline="",
            tags="login"
        )
        UIUtils.createRoundRect(
            self.canvas,
            300, 50,
            400, 500,
            radius=70,
            fill="#48426D",
            outline="",
            tags="login"
        )
        self.canvas.create_image(
            500, 120,
            image=self.images["logo"],
            tags="login"
        )

        UIUtils.createRoundRect(
            self.canvas,
            500, 190,
            150, 50,
            radius=30,
            fill="#4E4775",
            outline="",
            tags=("login", "signupBg")
        )
        UIUtils.createRoundRect(
            self.canvas,
            355, 195,
            300, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags=("login", "switchShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            350, 190,
            300, 50,
            radius=30,
            fill="#312C51",
            outline="",
            tags="login"
        )
        UIUtils.createRoundRect(
            self.canvas,
            350, 190,
            150, 50,
            radius=30,
            fill="#F0C38E",
            outline="",
            tags="login"
        )
        self.canvas.create_text(
            425, 215,
            text="sign-in",
            fill="#48426D",
            font=("koulen", 22),
            tags="login"
        )
        self.canvas.create_text(
            575, 215,
            text="SIGN-up",
            fill="#F0C38E",
            font=("koulen", 22),
            tags="login"
        )

        self.createFillUp(350, 280, self.username)
        self.createFillUp(350, 350, self.password)

        UIUtils.createRoundRect(
            self.canvas,
            430, 455,
            150, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags=("login", "loginButtonShadow")
        )
        UIUtils.createRoundRect(
            self.canvas,
            425, 450,
            150, 50,
            radius=30,
            fill="#F0C38E",
            outline="",
            tags="login"
        )
        self.canvas.create_text(
            500, 475,
            text="sign-in",
            font=("koulen", 22),
            fill="#48426D",
            tags="login"
        )
        UIUtils.createRoundRect(
            self.canvas,
            425, 450,
            150, 50,
            radius=30,
            fill="",
            outline="",
            tags=("login", "loginButton")
        )

        def onLoginClick(event):
            self.canvas.move("loginButtonShadow", -5, -5)

        def onLoginRelease(event):
            self.canvas.move("loginButtonShadow", 5, 5)
            accounts = Accounts()
            valid = accounts.authenticate(self.username[0], self.password[0])
            if not valid:
                return
            role = accounts.getRole(self.username[0])


        self.canvas.tag_bind("loginButton", "<Button-1>", onLoginClick)
        self.canvas.tag_bind("loginButton", "<ButtonRelease>", onLoginRelease)

    def createFillUp(self, x: int, y: int, data: list):
        tag = data[2]
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            300, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags=("login", f"shadow:{tag}")
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            300, 50,
            radius=30,
            fill="#F0C38E",
            outline="",
            tags="login"
        )
        self.canvas.create_line(
            x + 20, y + 40,
            x + 280, y + 40,
            fill="#48426D",
            width=2,
            tags=(f"line:{tag}", "selectorLine")
        )
        self.canvas.create_text(
            x + 20, y - 2,
            text=data[1],
            fill="#9C827D",
            font=("koulen", 22),
            anchor='nw',
            tags="input:" + tag
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            300, 50,
            radius=30,
            fill="",
            outline="",
            tags=tag
        )

        def onClick(event) -> None:
            self.canvas.focus_set()
            self.canvas.move(f"shadow:{tag}", -5, -5)

        def onRelease(event) -> None:
            self.canvas.move(f"shadow:{tag}", 5, 5)
            self.canvas.itemconfig("selectorLine", fill="#48426D")
            self.canvas.itemconfig(f"line:{tag}", fill="#FFFFFF")
            self.focusedField = tag

        self.canvas.tag_bind(tag, "<Button-1>", onClick)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", onRelease)

    def onKeyPress(self, event) -> None:
        if not self.focusedField:
            return

        fields = {
            "username": self.username,
            "password": self.password,
        }
        userInput = fields.get(self.focusedField)

        if not userInput: return

        if event.keysym == "BackSpace":
            userInput[0] = userInput[0][:-1]

        elif event.keysym == "Escape":
            self.focusedField = None
            self.canvas.itemconfig("selectorLine", fill="#48426D")

        elif event.keysym == "Return":
            self.focusedField = None
            self.canvas.itemconfig("selectorLine", fill="#48426D")

        elif len(event.char) == 1 and event.char.isprintable():
            char = event.char
            currentVal = userInput[0]

            if self.focusedField == "itemStock":
                if not char.isdigit():
                    return

            elif self.focusedField == "itemPrice":
                if char == ".":
                    if "." in currentVal:
                        return
                elif not char.isdigit():
                    return

            if self.focusedField == "itemTag" and len(userInput[0]) < 20:
                userInput[0] += char
            elif self.focusedField != "itemTag":
                userInput[0] += char

        display = userInput[0] if userInput[0] else userInput[1]
        color = "#48426D" if userInput[0] else "#9C827D"

        self.canvas.itemconfig(
            f"input:{userInput[2]}",
            text=display,
            fill=color
        )

    def onRaise(self):
        pass