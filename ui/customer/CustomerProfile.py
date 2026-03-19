import tkinter as tk

from PIL import ImageTk, Image

from dataManager.DataModels import Accounts
from ui import UIUtils, Codes
from ui.main import App
from util import Utils
from util.Utils import log


class CustomerProfile(tk.Frame):

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

        self.focusedField = None
        self.images = {}
        self.initImages()

    def unfocus(self, event):
        self.focusedField = None
        self.canvas.itemconfig(
            tagOrId="selectorLine",
            fill="#48426D"
        )

    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["buyer"] = ImageTk.PhotoImage(
            Image.open("../res/buyer_48426D.png").resize((40, 40), Image.Resampling.LANCZOS)
        )
        self.images["profile_chopped"] = ImageTk.PhotoImage(
            Image.open("../res/profile_chopped.png").resize((101, 101), Image.Resampling.LANCZOS)
        )
        self.images["buyer_F0C38E"] = ImageTk.PhotoImage(
            Image.open("../res/buyer_F0C38E.png").resize((30, 30), Image.Resampling.LANCZOS)
        )

    def initUi(self) -> None:
        self.canvas.bind("<Key>", self.onKeyPress)

        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )
        self.canvas.create_text(
            250, 105,
            text="Profile",
            font=(Utils.Fonts.KOULEN.value, 40),
            fill="#F0C38E"
        )
        self.canvas.create_text(
            750, 105,
            text="Statistics",
            font=(Utils.Fonts.KOULEN.value, 40),
            fill="#F0C38E"
        )

        self.createFillUp(93, 315, self.username)
        self.createFillUp(93, 390, self.password)

        self.canvas.create_oval(
            205, 175, 305, 275,
            fill="#363152",
            outline=""
        )
        self.canvas.create_oval(
            200, 170, 300, 270,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_image(
            251, 221,
            image=self.images["profile_chopped"]
        )

        UIUtils.createRoundRect(
            self.canvas,
            155, 470,
            200, 50,
            radius=30,
            fill="#363152",
            outline=""
        )
        UIUtils.createRoundRect(
            self.canvas,
            150, 465,
            200, 50,
            radius=30,
            fill="#48426D",
            outline=""
        )
        self.canvas.create_text(
            230, 492,
            text="Customer",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E"
        )
        self.canvas.create_image(
            320, 490,
            image=self.images["buyer_F0C38E"]
        )

        self.createDataEntry(575, 150, "items purchased:", self.profile["stats"]["items_purchased"])
        self.createDataEntry(575, 225, "amount spent:", self.profile["stats"]["amount_spent"])
        self.createDataEntry(575, 300, "balance:", self.profile["stats"]["balance"])

        UIUtils.createRoundRect(
            self.canvas,
            660, 385,
            180, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags="transactionShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            655, 380,
            180, 50,
            radius=30,
            fill="#F0C38E",
            outline="",
        )
        self.canvas.create_text(
            745, 405,
            text="transactions",
            font=(Utils.Fonts.KOULEN.value, 22),
            fill="#48426D",
        )
        UIUtils.createRoundRect(
            self.canvas,
            655, 380,
            180, 50,
            radius=30,
            fill="",
            outline="",
            tags="transactionsButton"
        )

        def onTransactionsClick(event):
            self.canvas.move("transactionShadow", -5, -5)

        def onTransactionsRelease(event):
            self.canvas.move("transactionShadow", 5, 5)


        self.canvas.tag_bind("transactionsButton", "<Button-1>", onTransactionsClick)
        self.canvas.tag_bind("transactionsButton", "<ButtonRelease-1>", onTransactionsRelease)

        UIUtils.createRoundRect(
            self.canvas,
            675, 465,
            150, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags="doneShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            670, 460,
            150, 50,
            radius=30,
            fill="#F0C38E",
            outline="",
        )
        self.canvas.create_text(
            745, 485,
            text="done",
            font=(Utils.Fonts.KOULEN.value, 22),
            fill="#48426D",
        )
        UIUtils.createRoundRect(
            self.canvas,
            670, 460,
            150, 50,
            radius=30,
            fill="",
            outline="",
            tags="doneButton"
        )

        def onDoneClick(event):
            self.canvas.move("doneShadow", -5, -5)
        def onDoneRelease(event):
            self.canvas.move("doneShadow", 5, 5)
            accounts = Accounts()
            if not self.username[0] and not self.password[0]:
                UIUtils.launchErrorWindow(
                    "Invalid input",
                    "Username and Password cannot be blank"
                )
                self.canvas.itemconfig("selectorLine", fill="#9A0000")
            elif accounts.checkPassword(self.password[0]) == Codes.ReturnCode.PASSWORD_INVALID:
                UIUtils.launchErrorWindow(
                    "Invalid input",
                    "Password must contain atleast 8 characters, number, and special characters"
                )
            else:
                accounts.modifyAccount(
                    username=self.username[1],
                    newUsername=self.username[0],
                    newPassword=self.password[0]
                )
                App.show("CustomerHome")

        self.canvas.tag_bind("doneButton", "<Button-1>", onDoneClick)
        self.canvas.tag_bind("doneButton", "<ButtonRelease-1>", onDoneRelease)

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
            tags=(f"line:{tag}", f"{tag}SelectorLine", "selectorLine")
        )
        self.canvas.create_text(
            x + 20, y - 2,
            text=data[1],
            fill="#48426D",
            font=(Utils.Fonts.MONO_MANIAC.value, 22),
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

    def createDataEntry(self, x: int, y: int, label: str, data: int) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            350, 50,
            radius=30,
            fill="#363152",
            outline="",
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            350, 50,
            radius=30,
            fill="#48426D",
            outline="",
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            230, 50,
            radius=30,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_text(
            x + 20, y,
            text=label,
            font=(Utils.Fonts.KOULEN.value, 22),
            fill="#48426D",
            anchor='nw',
        )
        self.canvas.create_text(
            x + 250, y,
            text=data,
            font=(Utils.Fonts.KOULEN.value, 22),
            fill="#F0C38E",
            anchor='nw',
        )


    def onKeyPress(self, event) -> None:
        if not self.focusedField:
            return

        userInput = {
                "username": self.username,
                "password": self.password,
            }.get(self.focusedField)

        if not userInput:
            return

        if event.keysym == "BackSpace":
            userInput[0] = userInput[0][:-1]

        elif event.keysym in ("Escape", "Return"):
            self.focusedField = None
            self.canvas.itemconfig("selectorLine", fill="#48426D")

        elif len(event.char) == 1 and event.char.isprintable():
            char = event.char
            userInput[0] += char

        self.canvas.itemconfig(
            f"input:{userInput[2]}",
            text=userInput[0] if userInput[0] else userInput[1],
            fill="#48426D" if userInput[0] else "#9C827D"
        )

    def onRaise(self) -> None:
        log("Raised CustomerProfile")

        self.canvas.delete("all")
        self.initImages()

        self.profile = Accounts().getAccount(App.customerScenes["CustomerHome"]["account"]["username"])
        self.username = [
            self.profile["username"],
            self.profile["username"],
            "username"
        ]
        self.password = [
            self.profile["password"],
            self.profile["password"],
            "password"
        ]

        self.focusedField = None

        self.initUi()