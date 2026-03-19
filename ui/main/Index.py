import tkinter as tk

from PIL import ImageTk, Image

from dataManager.DataModels import Accounts
from ui import UIUtils
from ui.Codes import ReturnCode, ThreatLevel
from ui.main import App
from util import Utils
from util.Utils import log, warn, logData


class Login(tk.Frame):

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
        self.canvas.tag_bind("bg", "<Button-1>", self.unfocus)

        self.images = {}
        self.initImages()

        self.focusedField = None
        self.username = ["", "Enter username", "username"]
        self.password = ["", "Enter password", "password"]

    def unfocus(self, event):
        self.focusedField = None
        self.canvas.itemconfig(
            tagOrId="selectorLine",
            fill="#48426D"
        )

    def initImages(self):
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["logo"] = ImageTk.PhotoImage(
            Image.open("../res/logo.png").resize((250, 60), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"],
            tags="bg"
        )
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
            fill="#3B365E",
            outline="",
            tags=("login", "signup", "signupBg")
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
            font=(Utils.Fonts.KOULEN.value, 22),
            tags="login"
        )
        self.canvas.create_text(
            575, 215,
            text="SIGN-up",
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 22),
            tags=("login", "signup")
        )
        UIUtils.createRoundRect(
            self.canvas,
            500, 190,
            150, 50,
            radius=30,
            fill="",
            outline="",
            tags=("login", "signup", "signupField")
        )

        def onSignUpClick(event):
            self.canvas.move("switchShadow", -5, -5)

        def onSignUpRelease(event):
            self.canvas.move("switchShadow", 5, 5)
            App.show("SignUp")

        def onSignUpHover(event):
            self.canvas.tag_raise("signup")

        def onSignUpLeave(event):
            self.canvas.tag_lower("signupBg")

        self.canvas.tag_bind("signupField", "<Button-1>", onSignUpClick)
        self.canvas.tag_bind("signupField", "<ButtonRelease-1>", onSignUpRelease)
        self.canvas.tag_bind("signupField", "<Enter>", onSignUpHover)
        self.canvas.tag_bind("signupField", "<Leave>", onSignUpLeave)

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
            font=(Utils.Fonts.KOULEN.value, 22),
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
            code = accounts.authenticate(self.username[0], self.password[0])
            if code != ReturnCode.SUCCESS:
                warn(f"Account authentication failed, exited with code: {code}")
                if not self.username[0]:
                    self.canvas.itemconfig(f"{self.username[2]}SelectorLine", fill="#9A0000")
                else:
                    self.canvas.itemconfig(f"{self.username[2]}SelectorLine", fill="#48426D")
                if not self.password[0]:
                    self.canvas.itemconfig(f"{self.password[2]}SelectorLine", fill="#9A0000")
                else:
                    self.canvas.itemconfig(f"{self.password[2]}SelectorLine", fill="#48426D")
                if not self.username[0] or not self.password[0]:
                    UIUtils.launchErrorWindow(
                        "Missing Input!",
                        f"Please fill up "
                        f"{"username" if not self.username[0] else ""}"
                        f"{"," if len(code) > 1 else ""}"
                        f" {"password" if not self.password[0] else ""}",
                    )
                elif code == ReturnCode.ACCOUNT_DOES_NOT_EXIST or code == ReturnCode.PASSWORD_INCORRECT:
                    UIUtils.launchErrorWindow(
                        "Incorrect Credentials",
                        "Username or Password is incorrect, please try again"
                    )
                self.focusedField = None
                return
            log(f"Login success for account: {self.username[0]}")
            if accounts.getRole(self.username[0]) == Accounts.Role.SELLER:
                App.sellerScenes["SellerHome"]["account"] = accounts.getAccount(self.username[0])
                App.show("SellerHome")
            else:
                App.customerScenes["CustomerHome"]["account"] = accounts.getAccount(self.username[0])
                App.show("CustomerHome")

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
            tags=(f"line:{tag}", f"{tag}SelectorLine", "selectorLine")
        )
        self.canvas.create_text(
            x + 20, y - 2,
            text=data[1],
            fill="#9C827D",
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

    def onRaise(self):
        log("Raised Login")

        self.canvas.delete("all")
        self.focusedField = None
        self.username = ["", "Enter username", "username"]
        self.password = ["", "Enter password", "password"]
        App.sellerScenes["SellerHome"]["account"] = {}

        self.initUi()

class SignUp(tk.Frame):

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
        self.canvas.tag_bind("bg", "<Button-1>", self.unfocus)

        self.icons = {}
        self.initIcons()
        self.images = {}
        self.initImages()

        self.focusedField = None
        self.username = ["", "Enter username", "username"]
        self.password = ["", "Enter password", "password"]
        self.role = "buyer"

        self.initUi()

    def unfocus(self, event):
        self.focusedField = None
        self.canvas.itemconfig(
            tagOrId="selectorLine",
            fill="#48426D"
        )

    def initIcons(self):
        self.icons["buyer"] = ImageTk.PhotoImage(
            Image.open("../res/buyer_48426D.png").resize((40, 40), Image.Resampling.LANCZOS)
        )
        self.icons["seller"] = ImageTk.PhotoImage(
            Image.open("../res/seller_48426D.png").resize((40, 40), Image.Resampling.LANCZOS)
        )

    def initImages(self):
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["logo"] = ImageTk.PhotoImage(
            Image.open("../res/logo.png").resize((250, 60), Image.Resampling.LANCZOS)
        )

    def initUi(self):
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"],
            tags="bg"
        )
        self.initLoginForm()

    def initLoginForm(self):
        UIUtils.createRoundRect(
            self.canvas,
            105, 55,
            800, 500,
            radius=70,
            fill="#25213D",
            outline=""
        )
        UIUtils.createRoundRect(
            self.canvas,
            100, 50,
            800, 500,
            radius=70,
            fill="#48426D",
            outline=""
        )
        self.canvas.create_image(
            500, 120,
            image=self.images["logo"]
        )

        UIUtils.createRoundRect(
            self.canvas,
            350, 190,
            150, 50,
            radius=30,
            fill="#3B365E",
            outline="",
            tags=("signIn", "signInBg")
        )
        UIUtils.createRoundRect(
            self.canvas,
            355, 195,
            300, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags="switchShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            350, 190,
            300, 50,
            radius=30,
            fill="#312C51",
            outline=""
        )
        UIUtils.createRoundRect(
            self.canvas,
            500, 190,
            150, 50,
            radius=30,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_text(
            425, 215,
            text="sign-in",
            fill="#F0C38E",
            font=(Utils.Fonts.KOULEN.value, 22),
            tags="signIn"
        )
        self.canvas.create_text(
            575, 215,
            text="SIGN-up",
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 22),
            tags="signIn"
        )
        UIUtils.createRoundRect(
            self.canvas,
            350, 190,
            150, 50,
            radius=30,
            fill="",
            outline="",
            tags=("signIn", "signInField")
        )

        def onSignUpClick(event):
            self.canvas.move("switchShadow", -5, -5)
        def onSignUpRelease(event):
            self.canvas.move("switchShadow", 5, 5)
            self.focusedField = None
            App.show("Login")

        def onSignUpHover(event):
            self.canvas.tag_raise("signIn")

        def onSignUpLeave(event):
            self.canvas.tag_lower("signInBg")

        self.canvas.tag_bind("signInField", "<Button-1>", onSignUpClick)
        self.canvas.tag_bind("signInField", "<ButtonRelease-1>", onSignUpRelease)
        self.canvas.tag_bind("signInField", "<Enter>", onSignUpHover)
        self.canvas.tag_bind("signInField", "<Leave>", onSignUpLeave)

        self.createFillUp(145, 280, self.username)
        self.createFillUp(145, 350, self.password)

        UIUtils.createRoundRect(
            self.canvas,
            600, 285,
            200, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags="roleShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            595, 280,
            200, 50,
            radius=30,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_text(
            670, 305,
            text="Buyer",
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 22),
            tags="roleText"
        )
        self.canvas.create_image(
            770, 305,
            image=self.icons["buyer"],
            tags="roleIcon"
        )
        UIUtils.createRoundRect(
            self.canvas,
            595, 280,
            200, 50,
            radius=30,
            fill="",
            outline="",
            tags="roleButton"
        )
        def onRoleButtonClick(event):
            self.canvas.move("roleShadow", -5, -5)
        def onRoleButtonRelease(event):
            self.canvas.move("roleShadow", 5, 5)
            self.role = "buyer" if self.role != "buyer" else "seller"
            self.canvas.itemconfig("roleText", text=self.role)
            self.canvas.itemconfig("roleIcon", image=self.icons[self.role])

        self.canvas.tag_bind("roleButton", "<Button-1>", onRoleButtonClick)
        self.canvas.tag_bind("roleButton", "<ButtonRelease-1>", onRoleButtonRelease)

        UIUtils.createRoundRect(
            self.canvas,
            430, 455,
            150, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags="signInButtonShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            425, 450,
            150, 50,
            radius=30,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_text(
            500, 475,
            text="sign-up",
            font=(Utils.Fonts.KOULEN.value, 22),
            fill="#48426D"
        )
        UIUtils.createRoundRect(
            self.canvas,
            425, 450,
            150, 50,
            radius=30,
            fill="",
            outline="",
            tags="signInButton"
        )

        def onLoginClick(event):
            self.canvas.move("signInButtonShadow", -5, -5)

        def onLoginRelease(event):
            self.canvas.move("signInButtonShadow", 5, 5)
            accounts = Accounts()
            result = accounts.createAccount(self.username[0], self.password[0], Accounts.Role(self.role))
            if result[0] != ReturnCode.SUCCESS:
                warn(f"Account creation failed, exited with code: {result}")
                if not self.username[0]:
                    self.canvas.itemconfig(f"{self.username[2]}SelectorLine", fill="#9A0000")
                else:
                    self.canvas.itemconfig(f"{self.username[2]}SelectorLine", fill="#48426D")
                if not self.password[0]:
                    self.canvas.itemconfig(f"{self.password[2]}SelectorLine", fill="#9A0000")
                else:
                    self.canvas.itemconfig(f"{self.password[2]}SelectorLine", fill="#48426D")
                if not self.username[0] or not self.password[0]:
                    UIUtils.launchErrorWindow(
                        "Missing Input!",
                        f"Please fill up "
                        f"{"username" if not self.username[0] else ""}"
                        f"{"," if result[0] is not tuple else ""}"
                        f" {"password" if not self.password[0] else ""}",
                    )
                elif result[0] == ReturnCode.ACCOUNT_ALREADY_EXISTS:
                    UIUtils.launchErrorWindow(
                        "Account Already Exists!",
                        "Username not available to use, please choose another username."
                    )
                elif result[0] == ReturnCode.PASSWORD_INVALID:
                    UIUtils.launchErrorWindow(
                        "Invalid input",
                        "Password must contain atleast 8 characters, number, and special characters"
                    )
                return
            if Accounts.Role(self.role) == Accounts.Role.SELLER:
                App.sellerScenes["SellerHome"]["account"] = result[-1]
                App.show("SellerHome")
            else:
                App.customerScenes["CustomerHome"]["account"] = accounts.getAccount(self.username[0])
                App.show("CustomerHome")

        self.canvas.tag_bind("signInButton", "<Button-1>", onLoginClick)
        self.canvas.tag_bind("signInButton", "<ButtonRelease>", onLoginRelease)

    def createFillUp(self, x: int, y: int, data: list):
        tag = data[2]
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            300, 50,
            radius=30,
            fill="#363152",
            outline="",
            tags=f"shadow:{tag}"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            300, 50,
            radius=30,
            fill="#F0C38E",
            outline=""
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
            fill="#9C827D",
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

    def onRaise(self):
        log("Raised SignUp")

        self.canvas.delete("all")
        self.focusedField = None
        self.username = ["", "Enter username", "username"]
        self.password = ["", "Enter password", "password"]
        self.role = "buyer"

        self.initUi()