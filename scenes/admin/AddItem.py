import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog

from PIL import ImageTk, Image

from dataManager import FileHandler as FH, DataModels as DM
from dataManager.DataModels import Items
from scenes import UIUtils
from scenes import App
from util.Utils import log, warn

class AddItem(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#48426D")

        self.image = ""
        self.icons = {}
        self.icons["add_48426D"] = ImageTk.PhotoImage(
            Image.open("../res/add_48426D.png").resize((25, 25), Image.Resampling.LANCZOS)
        )
        self.icons["add_9C827D"] = ImageTk.PhotoImage(
            Image.open("../res/add_9C827D.png").resize((80, 80), Image.Resampling.LANCZOS)
        )

        self.itemName = ["", "Enter Item Name", "itemName"]
        self.itemPrice = ["", "Enter item price", "itemPrice"]
        self.itemStock = ["", "Enter item stock", "itemStock"]
        self.itemTag = ["", "Enter item tag", "itemTag", []]
        self.focusedField = None

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
            outline="",
            tags="bg"
        )
        self.initHeader()
        self.initForm()
        self.initPhoto()
        self.initOperations()

        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Key>", self.onKeyPress)
        self.canvas.tag_bind("bg", "<Button-1>", self.reset)

    def reset(self, event):
        self.itemName = ["", "Enter Item Name", "itemName"]
        self.itemPrice = ["", "Enter item price", "itemPrice"]
        self.itemStock = ["", "Enter item stock", "itemStock"]
        self.itemTag = ["", "Enter item tag", "itemTag", []]
        self.focusedField = None
        self.image = ""
        self.canvas.itemconfig("selectorLine", fill="#48426D")

    def initHeader(self):
        self.canvas.create_rectangle(
            0, 0,
            1000, 75,
            fill="#363152",
            outline="",
            tags="search"
        )
        self.canvas.create_rectangle(
            0, 0,
            1000, 70,
            fill="#312C51",
            outline="",
            tags="search"
        )
        self.canvas.create_text(
            20, 0,
            text="Add Item",
            font=("koulen", 30),
            fill="#F0C38E",
            anchor='nw'
        )

    def initForm(self):
        self.canvas.create_text(
            30, 80,
            text="Item Details:",
            font=("koulen", 24),
            fill="#F0C38E",
            anchor='nw'
        )
        self.canvas.create_text(
            30, 385,
            text="Item Tags:",
            font=("koulen", 24),
            fill="#F0C38E",
            anchor='nw'
        )
        self.createInputField(
            30, 140,
            "Item name:",
            self.itemName[1],
            self.itemName[2]
        )
        self.createInputField(
            30, 205,
            "Item price:",
            self.itemPrice[1],
            self.itemPrice[2]
        )
        self.createInputField(
            30, 270,
            "Item stock:",
            self.itemStock[1],
            self.itemStock[2]
        )
        self.createTagInputField(30, 335)

    def createInputField(self, x: int, y: int, label: str, placeholder: str, tag: str) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            600, 40,
            radius=20,
            fill="#363152",
            outline="",
            tags=f"shadow:{tag}"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            600, 40,
            radius=20,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_line(
            x + 160, y + 34,
            x + 580, y + 34,
            fill="#48426D",
            width=2,
            tags=(f"line:{tag}", "selectorLine")
        )
        self.canvas.create_text(
            x + 170, y - 4,
            text=placeholder,
            fill="#9C827D",
            font=("koulen", 21),
            anchor='nw',
            tags="input:" + tag
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            150, 40,
            radius=20,
            fill="#312C51",
            outline=""
        )
        self.canvas.create_text(
            x + 20, y - 4,
            text=label,
            fill="#F0C38E",
            font=("koulen", 21),
            anchor='nw'
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            600, 40,
            radius=20,
            fill="",
            outline="",
            tags=tag
        )
        
        def onClick(event):
            log(f"Clicked on {tag}")
            self.focusedField = tag
            self.canvas.focus_set()
            self.canvas.move(f"shadow:{tag}", -5, -5)
            self.canvas.itemconfig("selectorLine", fill="#48426D")
            self.canvas.itemconfig(f"line:{tag}", fill="#FFFFFF")
        def onRelease(event):
            self.canvas.move(f"shadow:{tag}", 5, 5)

        self.canvas.tag_bind(tag, "<Button-1>", onClick)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", onRelease)

    def createTagInputField(self, x: int, y: int) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            550, 40,
            radius=20,
            fill="#363152",
            outline="",
            tags=f"shadow:itemTag"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            550, 40,
            radius=20,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_line(
            x + 160, y + 34,
            x + 530, y + 34,
            fill="#48426D",
            width=2,
            tags=("line:itemTag", "selectorLine")
        )
        self.canvas.create_text(
            x + 170, y - 4,
            text="Enter Item Tag",
            fill="#9C827D",
            font=("koulen", 21),
            anchor='nw',
            tags="input:itemTag"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            150, 40,
            radius=20,
            fill="#312C51",
            outline=""
        )
        self.canvas.create_text(
            x + 20, y - 4,
            text="Tag:",
            fill="#F0C38E",
            font=("koulen", 21),
            anchor='nw'
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            550, 40,
            radius=20,
            fill="",
            outline="",
            tags="itemTag"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x + 565, y + 5,
            40, 40,
            radius=20,
            fill="#363152",
            outline="",
            tags="addTagShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            x + 560, y,
            40, 40,
            radius=20,
            fill="#F0C38E",
            outline=""
        )
        self.canvas.create_image(
            x + 580, y + 20,
            image=self.icons["add_48426D"],
            anchor="center",
        )
        UIUtils.createRoundRect(
            self.canvas,
            x + 560, y,
            40, 40,
            radius=20,
            fill="",
            outline="",
            tags="addTag"
        )

        def onClick(event):
            log(f"Clicked on itemTag")
            self.focusedField = "itemTag"
            self.canvas.focus_set()
            self.canvas.move(f"shadow:itemTag", -5, -5)
            self.canvas.itemconfig("selectorLine", fill="#48426D")
            self.canvas.itemconfig("line:itemTag", fill="#FFFFFF")

        def onRelease(event):
            self.canvas.move(f"shadow:itemTag", 5, 5)

        self.canvas.tag_bind("itemTag", "<Button-1>", onClick)
        self.canvas.tag_bind("itemTag", "<ButtonRelease-1>", onRelease)

        def onAddClick(event):
            self.canvas.move("addTagShadow", -5, -5)
            if self.itemTag[0] and self.itemTag[0].lower() not in self.itemTag[3]:
                self.itemTag[3].append(self.itemTag[0].lower())
                self.canvas.itemconfig("input:itemTag", fill="#9C827D", text="Enter Item tag")
                self.itemTag[0] = ""
            log(self.itemTag[3])
            self.initTags()

        def onAddRelease(event):
            self.canvas.move("addTagShadow", 5, 5)

        self.canvas.tag_bind("addTag", "<Button-1>", onAddClick)
        self.canvas.tag_bind("addTag", "<ButtonRelease-1>", onAddRelease)

    def initTags(self):
        font = tkFont.Font(family="koulen", size=21)
        maxWidth = 600
        yLevel = 0
        self.canvas.delete("itemTagEntry")
        lastX = 15
        for tag in self.itemTag[3]:
            width = font.measure(tag)
            if lastX + width > maxWidth:
                yLevel += 1
                lastX = 15
            lastX = self.createTag(
                lastX + 15,
                445 + (55 * yLevel),
                tag,
                font
            )

    def createTag(self, x: int, y: int, tag: str, font: tkFont.Font) -> int:
        width = font.measure(tag)

        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            width + 20, 40,
            radius=20,
            fill="#363152",
            outline="",
            tags=("itemTagEntry", f"tag:{tag}", f"shadow:{tag}"),
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            width + 20, 40,
            radius=20,
            fill="#312C51",
            outline="",
            tags=("itemTagEntry", f"tag:{tag}"),
        )
        self.canvas.create_text(
            x + int(width / 2) + 10, y + 20,
            text=tag,
            font=font,
            fill="#F0C38E",
            anchor="center",
            tags=("itemTagEntry", f"tag:{tag}"),
        )

        def onClick(event):
            self.canvas.move(f"shadow:{tag}", -5, -5)

        def deleteItem(event):
            self.canvas.move(f"shadow:{tag}", 5, 5)
            self.canvas.delete(f"tag:{tag}")
            self.itemTag[3].remove(tag)
            self.initTags()

        self.canvas.tag_bind(f"tag:{tag}", "<Button-1>", onClick)
        self.canvas.tag_bind(f"tag:{tag}", "<ButtonRelease-1>", deleteItem)

        return x + width + 20

    def initPhoto(self):
        UIUtils.createRoundRect(
            self.canvas,
            675, 145,
            280, 305,
            radius=40,
            fill="#363152",
            outline="",
            tags="uploadPhotoShadow",
        )
        UIUtils.createRoundRect(
            self.canvas,
            670, 140,
            280, 305,
            radius=40,
            fill="#F0C38E",
            outline=""
        )
        UIUtils.createRoundRect(
            self.canvas,
            670, 365,
            280, 80,
            radius=40,
            fill="#312C51",
            outline=""
        )
        self.canvas.create_rectangle(
            670, 365,
            950, 400,
            fill="#312C51",
            outline=""
        )
        self.canvas.create_text(
            810, 405,
            text="Cover photo",
            font=("koulen", 24),
            anchor="center",
            fill="#F0C38E",
        )
        self.canvas.create_image(
            810, 250,
            image=self.icons["add_9C827D"]
        )
        self.canvas.create_text(
            810, 320,
            text="Upload photo",
            font=("koulen", 18),
            fill="#9C827D",
            anchor="center",
        )
        UIUtils.createRoundRect(
            self.canvas,
            670, 140,
            280, 305,
            radius=40,
            fill="",
            outline="",
            tags="uploadPhoto",
        )

        def onClick(event):
            self.canvas.move("uploadPhotoShadow", -5, -5)
            imageTypes = [
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png")
            ]
            self.image = filedialog.askopenfilename(
                title="Select a file to upload",
                filetypes=imageTypes
            )

        def onRelease(event):
            self.canvas.move("uploadPhotoShadow", 5, 5)

        self.canvas.tag_bind("uploadPhoto", "<Button-1>", onClick)
        self.canvas.tag_bind("uploadPhoto", "<ButtonRelease-1>", onRelease)

    def initOperations(self):
        UIUtils.createRoundRect(
            self.canvas,
            715, 505,
            100, 40,
            fill="#363152",
            outline="",
            tags="cancelButtonShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            710, 500,
            100, 40,
            fill="#F0C38E",
            outline="",
        )
        self.canvas.create_text(
            760, 520,
            text="Cancel",
            font=("koulen", 21),
            fill="#48426D",
            anchor="center",
        )
        UIUtils.createRoundRect(
            self.canvas,
            710, 500,
            100, 40,
            fill="",
            outline="",
            tags="cancelButton"
        )

        def cancelClick(event):
            self.canvas.move("cancelButtonShadow", -5, -5)
        def cancelRelease(event):
            self.canvas.move("cancelButtonShadow", 5, 5)
            self.reset("")
            App.show("ItemManager")

        self.canvas.tag_bind("cancelButton", "<Button-1>", cancelClick)
        self.canvas.tag_bind("cancelButton", "<ButtonRelease-1>", cancelRelease)

        UIUtils.createRoundRect(
            self.canvas,
            830, 505,
            80, 40,
            fill="#363152",
            outline="",
            tags="doneButtonShadow"
        )
        UIUtils.createRoundRect(
            self.canvas,
            825, 500,
            80, 40,
            fill="#F0C38E",
            outline="",
        )
        self.canvas.create_text(
            865, 520,
            text="Done",
            font=("koulen", 21),
            fill="#48426D",
            anchor="center",
        )
        UIUtils.createRoundRect(
            self.canvas,
            825, 500,
            80, 40,
            fill="",
            outline="",
            tags="doneButton"
        )

        def doneClick(event):
            self.canvas.move("doneButtonShadow", -5, -5)
        def doneRelease(event):
            self.canvas.move("doneButtonShadow", 5, 5)
            self.saveData()
            App.show("ItemManager")

        self.canvas.tag_bind("doneButton", "<Button-1>", doneClick)
        self.canvas.tag_bind("doneButton", "<ButtonRelease-1>", doneRelease)

    def saveData(self):
        items = Items()
        item = items.addItem(
            self.itemName[0],
            float(self.itemPrice[0]),
            int(self.itemStock[0]),
            self.itemTag[3]
        )
        FH.clone(self.image, f"../Database/images/{item["item_id"]}.{self.image.split('.').pop()}")

    def onKeyPress(self, event):
        if not self.focusedField:
            return

        fields = {
            "itemName": self.itemName,
            "itemPrice": self.itemPrice,
            "itemStock": self.itemStock,
            "itemTag": self.itemTag
        }
        userInput = fields.get(self.focusedField)

        if not userInput: return

        if event.keysym == "BackSpace":
            userInput[0] = userInput[0][:-1]

        elif event.keysym == "Escape":
            self.focusedField = None
            self.canvas.itemconfig("selectorLine", fill="#48426D")

        elif event.keysym == "Return":
            if self.focusedField == "itemTag" and userInput[0] not in userInput[3]:
                userInput[3].append(userInput[0])
                userInput[0] = ""
                self.initTags()
                log(f"Tags updated: {userInput[3]}")
            else:
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