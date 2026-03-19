import calendar
import tkinter as tk
from datetime import datetime, date
from typing import Callable

from PIL import ImageTk, Image

from dataManager.DataSummaries import SalesSummaries
from ui import UIUtils
from ui.main import App
from util import Utils
from util.Utils import log, logData


class Summaries(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#48426D")

        self.controller = controller
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=800,
            bg="#48426D",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.images = {}
        self.initImages()

        calendar.setfirstweekday(calendar.SUNDAY)
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.week = date(self.year, self.month, self.day).isocalendar()[1]
        self.weekLabel = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.selectedYear = self.year
        self.selectedMonth = self.month
        self.selectedDay = self.day
        self.row = 0
        self.mwPillData = [0]
        self.activeGraph = ""

    def initImages(self) -> None:
        self.images["bg"] = ImageTk.PhotoImage(
            Image.open("../res/bg.png").resize((1000, 600), Image.Resampling.LANCZOS)
        )
        self.images["blackFilter"] = ImageTk.PhotoImage(
            Image.open("../res/black_filter.png")
        )
        self.images["calendar"] = ImageTk.PhotoImage(
            Image.open("../res/calendar.png").resize((30, 30), Image.Resampling.LANCZOS)
        )
        self.images["arrowRight"] = ImageTk.PhotoImage(
            Image.open("../res/arrow.png").resize((20, 20), Image.Resampling.LANCZOS)
        )
        self.images["arrowLeft"] = ImageTk.PhotoImage(
            Image.open("../res/arrow.png").resize((20, 20), Image.Resampling.LANCZOS).rotate(180 % 360)
        )
        self.images["check"] = ImageTk.PhotoImage(
            Image.open("../res/check.png").resize((23, 24), Image.Resampling.LANCZOS)
        )

    def initUi(self) -> None:
        self.canvas.create_image(
            500, 300,
            image=self.images["bg"]
        )
        self.canvas.create_rectangle(
            0, 515,
            1000, 520,
            fill="#363152",
            outline=""
        )
        self.canvas.create_rectangle(
            0, 520,
            1000, 600,
            fill="#48426D",
            outline=""
        )
        UIUtils.createRoundRect(
            self.canvas,
            5, 5, 100, 30,
            radius=15,
            fill="#363152",
            outline="",
            tags="tooltip"
        )
        UIUtils.createRoundRect(
            self.canvas,
            0, 0, 100, 30,
            radius=15,
            fill="#F0C38E",
            outline="",
            tags="tooltip"
        )
        self.canvas.create_text(
            50, 15,
            text="",
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 13),
            tags=("tooltip", "tooltipText")
        )
        UIUtils.createRoundRect(
            self.canvas,
            5, 45, 100, 30,
            radius=15,
            fill="#363152",
            outline="",
            tags="tooltip"
        )
        UIUtils.createRoundRect(
            self.canvas,
            0, 40, 100, 30,
            radius=15,
            fill="#F0C38E",
            outline="",
            tags="tooltip"
        )
        self.canvas.create_text(
            50, 55,
            text="",
            fill="#48426D",
            font=(Utils.Fonts.KOULEN.value, 13),
            tags=("tooltip", "tooltipTextDate")
        )

        self.canvas.tag_lower("tooltip")

        def done():
            App.show("SellerHome")

        self.createButton(
            425, 535,
            150, 50,
            "done",
            "exit",
            done
        )

    def initGraphArea(self, graphName: str, xAxisLabel: str, xData: int | list[str], ySize: int, yHighest: int, points: list[int]) -> None:
        UIUtils.createRoundRect(
            self.canvas,
            55, 35,
            900, 450,
            radius=40,
            fill="#363152",
            outline="",
            tags="graph"
        )
        UIUtils.createRoundRect(
            self.canvas,
            50, 30,
            900, 450,
            radius=40,
            fill="#48426D",
            outline="",
            tags="graph"
        )
        UIUtils.createRoundRect(
            self.canvas,
            50, 30,
            900, 75,
            radius=40,
            fill="#312C51",
            outline="",
            tags="graph"
        )
        self.canvas.create_rectangle(
            50, 50,
            950, 105,
            fill="#312C51",
            outline="",
            tags="graph"
        )

        def openCalendar():
            self.initCalendar(calendar.monthcalendar(self.year, self.month))

        self.createButton(
            880, 45,
            50, 50,
            self.images["calendar"],
            "calendarButton",
            openCalendar,
            tags=("graph", )
        )
        self.canvas.create_text(
            500, 65,
            text=graphName,
            font=(Utils.Fonts.KOULEN.value, 30),
            fill="#F0C38E",
            anchor="center",
            tags=("graphName", "graph")
        )
        graphX = 170
        graphY = 145
        graphWidth = 750
        graphHeight = 250
        UIUtils.createRoundRect(
            self.canvas,
            graphX, graphY,
            graphWidth, graphHeight,
            radius=30,
            fill="#363152",
            outline="",
            tags="graph"
        )

        dashLength = 7
        gapLength = 5
        endX = graphWidth + graphX
        yGap = graphHeight / (ySize + 1)
        endY = graphHeight + graphY
        xSize = xData if xData.__class__ == int else len(xData)
        xGap = graphWidth / (xSize + 1)

        for i in range(ySize):
            y = graphY + ((i + 1) * yGap)
            currentX = graphX
            while currentX < endX:
                nextX = min(currentX + dashLength, endX)
                self.canvas.create_line(
                    currentX, y,
                    nextX, y,
                    fill="#614C63",
                    width=2,
                    tags="graph"
                )
                currentX += dashLength + gapLength

            self.canvas.create_text(
                graphX - 10, y,
                text=f"₱{round(((ySize - i) / ySize) * yHighest):,.2f}",
                font=(Utils.Fonts.KOULEN.value, 15),
                fill="#F0C38E",
                anchor="e",
                tags="graph"
            )

        for i in range(xSize):
            x = graphX + ((i + 1) * xGap)
            currentY = graphY
            while currentY < endY:
                nextY = min(currentY + dashLength, endY)
                self.canvas.create_line(
                    x, currentY,
                    x, nextY,
                    fill="#614C63",
                    width=2,
                    tags="graph"
                )
                currentY += dashLength + gapLength

            self.canvas.create_text(
                x, 410,
                text=(i + 1) if xData.__class__ == int else xData[i],
                font=(Utils.Fonts.KOULEN.value, 15),
                fill="#F0C38E",
                anchor="center",
                tags="graph"
            )

        self.canvas.create_text(
            graphX + (graphWidth / 2), 450,
            text=xAxisLabel,
            font=(Utils.Fonts.KOULEN.value, 30),
            fill="#F0C38E",
            tags="graph"
        )

        yScale = (yGap * ySize) / yHighest

        for i in range(len(points) - 1):
            currX = graphX + ((i + 1) * xGap)
            nextX = graphX + ((i + 2) * xGap)
            currY = (graphY + graphHeight) - (points[i] * yScale)
            nextY = (graphY + graphHeight) - (points[i + 1] * yScale)

            self.canvas.create_line(
                currX, currY,
                nextX, nextY,
                fill="#00FFFF",
                width=3,
                capstyle="round",
                joinstyle="round",
                tags="graph"
            )

        for i in range(len(points)):
            currX = graphX + ((i + 1) * xGap)
            currY = (graphY + graphHeight) - (points[i] * yScale)
            r = 7
            self.canvas.create_oval(
                currX - r, currY - r,
                currX + r, currY + r,
                fill="#F0C38E", outline="",
                tags=(f"point{i}", "graph")
            )

            def onHover(event, value, day):
                self.canvas.itemconfigure("tooltipTextDate", text=f"{calendar.month_abbr[self.month]}. {day}, {self.year}")
                self.canvas.itemconfigure("tooltipText", text=f"₱{value:,.2f}")

                tx = event.x + 10
                ty = event.y + 10

                self.canvas.moveto("tooltip", tx, ty)
                self.canvas.tag_raise("tooltip")

            def onLeave(event):
                self.canvas.tag_lower("tooltip")
                pass

            self.canvas.tag_bind(f"point{i}", "<Enter>", lambda e, p=points[i], d=i + 1: onHover(e, p, d))
            self.canvas.tag_bind(f"point{i}", "<Leave>", onLeave)

    def initCalendar(self, cldr: list[list]):
        self.canvas.create_image(
            500, 300,
            image=self.images["blackFilter"],
            tags="calendar"
        )
        UIUtils.createRoundRect(
            self.canvas,
            535, 120,
            400, 370,
            radius=40,
            fill="#363152",
            outline="",
            tags="calendar"
        )
        UIUtils.createRoundRect(
            self.canvas,
            530, 115,
            400, 370,
            radius=40,
            fill="#48426D",
            outline="",
            tags="calendar"
        )
        UIUtils.createRoundRect(
            self.canvas,
            530, 115,
            400, 75,
            radius=40,
            fill="#312C51",
            outline="",
            tags="calendar"
        )
        self.canvas.create_rectangle(
            530, 140,
            930, 190,
            fill="#312C51",
            outline="",
            tags="calendar"
        )
        self.canvas.create_rectangle(
            530, 190,
            930, 195,
            fill="#363152",
            outline="",
            tags="calendar"
        )
        self.canvas.create_text(
            730, 158,
            text=f"{calendar.month_name[self.month]} - {self.year}",
            font=(Utils.Fonts.KOULEN.value, 27),
            fill="#F0C38E",
            tags=("calendar", "currentCalendarPage")
        )
        self.canvas.create_text(
            630, 225,
            text="s",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            670, 225,
            text="m",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            710, 225,
            text="t",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            750, 225,
            text="w",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            790, 225,
            text="th",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            830, 225,
            text="f",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )
        self.canvas.create_text(
            870, 225,
            text="s",
            font=(Utils.Fonts.KOULEN.value, 20),
            fill="#F0C38E",
            tags="calendar"
        )

        def next():
            self.month += 1
            if self.month > 12:
                self.year += 1
                self.month = 1
            self.canvas.delete("calendar")
            self.initCalendar(calendar.monthcalendar(self.year, self.month))

        self.createButton(
            550, 250,
            30, 30,
            self.images["arrowRight"],
            "next",
            next,
            r=20,
            tags=("calendar",)
        )

        def previous():
            self.month -= 1
            if self.month < 1:
                self.year -= 1
                self.month = 12
            self.canvas.delete("calendar")
            self.initCalendar(calendar.monthcalendar(self.year, self.month))

        self.createButton(
            550, 287,
            30, 30,
            self.images["arrowLeft"],
            "previous",
            previous,
            r=20,
            tags=("calendar",)
        )

        def done():
            self.canvas.delete("calendar")
            if self.mwPillData[0] == 0:
                summarizer = SalesSummaries()
                currentUser = App.sellerScenes["SellerHome"]["account"]["username"]

                points = summarizer.getMonthlySales(
                    currentUser,
                    self.year,
                    self.month,
                )
                highest = summarizer.getHighestValue(points)

                self.initGraphArea(
                    f"Monthly Sales   |   {calendar.month_name[self.month]} - {self.year}",
                    "DAY",
                    31,
                    5,
                    yHighest=highest,
                    points=points
                )
            else:
                summarizer = SalesSummaries()
                currentUser = App.sellerScenes["SellerHome"]["account"]["username"]

                self.week = date(
                    self.selectedYear,
                    self.selectedMonth,
                    self.selectedDay
                ).isocalendar()[1]
                points = summarizer.getWeeklySales(
                    currentUser,
                    self.selectedYear,
                    self.week
                )
                highest = summarizer.getHighestValue(points)

                self.initGraphArea(
                    f"Weekly Sales   |   Week: {self.row + 1}   |   {calendar.month_name[self.month]} - {self.year}",
                    "DAY",
                    self.weekLabel,
                    5,
                    yHighest=highest,
                    points=points
                )

        self.createButton(
            550, 342,
            30, 30,
            self.images["check"],
            "done",
            done,
            r=20,
            tags=("calendar",)
        )

        def switch():
            if self.mwPillData[0] == 0:
                self.activeGraph = "month"
                self.canvas.itemconfig("dayButtonFg", fill="#48426D")
                self.canvas.itemconfig("dayButtonText", fill="#F0C38E")
            else:
                self.activeGraph = "week"
                self.canvas.itemconfig("dayButtonFg", fill="#F0C38E")
                self.canvas.itemconfig("dayButtonText", fill="#48426D")

        self.createPillButton(
            550, 398,
            30, 60,
            "m", "w",
            "mw",
            switch,
            self.mwPillData,
            orientation="vertical",
            r=20,
            font=(Utils.Fonts.KOULEN.value, 15),
            tags=("calendar",)
        )

        for y in range(len(cldr)):
            for x in range(len(cldr[y])):
                if cldr[y][x] == 0:
                    continue

                def onClick(cd: list[list], day: int, month: int, year: int, row: int):

                    if self.mwPillData[0] == 1:
                        self.canvas.itemconfig("dayButtonFg", fill="#F0C38E")
                        self.canvas.itemconfig("dayButtonText", fill="#48426D")
                        self.canvas.itemconfig(f"row{row}Fg", fill="#F1AA9B")
                        self.canvas.itemconfig(f"row{row}Text", fill="#48426D")
                        self.row = row
                        self.week = date(year, month, day).isocalendar()[1]
                        self.selectedWeek = cd[y]
                        self.selectedYear = year
                        self.selectedMonth = month
                        self.selectedDay = day

                day = cldr[y][x]
                self.createButton(
                    615 + (x * 40),
                    250 + (y * 37),
                    30, 30,
                    f"{day}",
                    f"day{day}",
                    lambda cd=cldr, d=day, m=self.month, y=self.year, r=y: onClick(cldr, d, m, y, r),
                    r=20,
                    font=(Utils.Fonts.KOULEN.value, 15),
                    tags=("calendar", "dayButton", f"row{y}")
                )

        if self.mwPillData[0] == 0:
            self.activeGraph = "month"
            self.canvas.itemconfig("dayButtonFg", fill="#48426D")
            self.canvas.itemconfig("dayButtonText", fill="#F0C38E")
            self.canvas.moveto(f"mwActive", 550, 398)
            self.canvas.itemconfig("mwActiveLabel1", fill="#48426D")
            self.canvas.itemconfig("mwActiveLabel2", fill="#F0C38E")
        else:
            self.activeGraph = "week"
            self.canvas.itemconfig("dayButtonFg", fill="#F0C38E")
            self.canvas.itemconfig("dayButtonText", fill="#48426D")
            self.canvas.moveto(f"mwActive", 550, 428)
            self.canvas.itemconfig("mwActiveLabel1", fill="#F0C38E")
            self.canvas.itemconfig("mwActiveLabel2", fill="#48426D")
            if self.selectedYear == self.year and self.selectedMonth == self.month:
                self.canvas.itemconfig("dayButtonFg", fill="#F0C38E")
                self.canvas.itemconfig("dayButtonText", fill="#48426D")
                self.canvas.itemconfig(f"row{self.row}Fg", fill="#F1AA9B")
                self.canvas.itemconfig(f"row{self.row}Text", fill="#48426D")

    def createButton(self, x: int, y: int, w: int, h: int, label: str | ImageTk.PhotoImage, tag: str,
                     function: Callable, r: int=30, splinesteps=36, font=(Utils.Fonts.KOULEN.value, 25),
                     tags: tuple=()):
        UIUtils.createRoundRect(
            self.canvas,
            x + 5, y + 5,
            w, h,
            radius=r,
            fill="#363152",
            outline="",
            splinesteps=splinesteps,
            tags=(f"{tag}Shadow", ) + tags
        )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=r,
            fill="#F0C38E",
            outline="",
            splinesteps=splinesteps,
            tags = (f"{tag}Fg", ) + tuple(f"{tag}Fg" for tag in tags) + tags
        )
        if label.__class__ == str:
            self.canvas.create_text(
                x + int(w / 2),
                y + int(h / 2),
                text=label,
                font=font,
                fill="#48426D",
                tags=tags + tuple(f"{tag}Text" for tag in tags)
            )
        elif label.__class__ == ImageTk.PhotoImage:
            self.canvas.create_image(
                x + int(w / 2),
                y + int(h / 2),
                image=label,
                tags=tags
            )
        UIUtils.createRoundRect(
            self.canvas,
            x, y,
            w, h,
            radius=r,
            fill="",
            outline="",
            splinesteps=splinesteps,
            tags=(f"{tag}Button", ) + tags
        )

        def onClick(event):
            self.canvas.move(f"{tag}Shadow", -5, -5)

        def onRelease(event):
            self.canvas.move(f"{tag}Shadow", 5, 5)
            function()

        self.canvas.tag_bind(f"{tag}Button", "<Button-1>", onClick)
        self.canvas.tag_bind(f"{tag}Button", "<ButtonRelease-1>", onRelease)

    def createPillButton(self, x: int, y: int, w: int, h: int, label1: str | ImageTk.PhotoImage, label2: str | ImageTk.PhotoImage,
                     tag: str, function: Callable, data: list, orientation="vertical", r: int=30, splinesteps=36, font=(Utils.Fonts.KOULEN.value, 25),
                     tags: tuple=()):

        if orientation == "vertical":
            UIUtils.createRoundRect(
                self.canvas,
                x + 5, y + 5,
                w, h,
                radius=r,
                fill="#363152",
                outline="",
                splinesteps=splinesteps,
                tags=(f"{tag}Shadow", ) + tags
            )
            UIUtils.createRoundRect(
                self.canvas,
                x, y,
                w, h,
                radius=r,
                fill="#48426D",
                outline="",
                splinesteps=splinesteps,
                tags=tags
            )
            UIUtils.createRoundRect(
                self.canvas,
                x, y,
                w, h // 2,
                radius=r,
                fill="#F0C38E",
                outline="",
                splinesteps=splinesteps,
                tags=(f"{tag}Active", ) + tags,
            )
            if label1.__class__ == str:
                self.canvas.create_text(
                    x + int(w / 2),
                    y + int(h / 4),
                    text=label1,
                    font=font,
                    fill="#48426D",
                    tags=(f"{tag}ActiveLabel1", ) + tags,
                )
            elif label1.__class__ == ImageTk.PhotoImage:
                self.canvas.create_image(
                    x + int(w / 2),
                    y + int(h / 4),
                    image=label1,
                    tags=(f"{tag}ActiveLabel1", ) + tags,
                )
            if label2.__class__ == str:
                self.canvas.create_text(
                    x + int(w / 2),
                    y + int(h / 4) + int(h / 2),
                    text=label2,
                    font=font,
                    fill="#F0C38E",
                    tags=(f"{tag}ActiveLabel2", ) + tags,
                )
            elif label2.__class__ == ImageTk.PhotoImage:
                self.canvas.create_image(
                    x + int(w / 2),
                    y + int(h / 4) + int(h / 2),
                    image=label2,
                    tags=(f"{tag}ActiveLabel2", ) + tags,
                )
            UIUtils.createRoundRect(
                self.canvas,
                x, y,
                w, h,
                radius=r,
                fill="",
                outline="",
                splinesteps=splinesteps,
                tags=(f"{tag}Button", ) + tags
            )

            def onClick(event):
                self.canvas.move(f"{tag}Shadow", -5, -5)

            def onRelease(event):
                self.canvas.move(f"{tag}Shadow", 5, 5)
                data[0] = 0 if data[0] == 1 else 1
                if data[0] == 0:
                    if label1.__class__ == str:
                        self.canvas.itemconfig(f"{tag}ActiveLabel1", fill="#48426D")
                    if label2.__class__ == str:
                        self.canvas.itemconfig(f"{tag}ActiveLabel2", fill="#F0C38E")
                        self.canvas.moveto(f"mwActive", 550, 398)
                else:
                    if label1.__class__ == str:
                        self.canvas.itemconfig(f"{tag}ActiveLabel1", fill="#F0C38E")
                    if label2.__class__ == str:
                        self.canvas.itemconfig(f"{tag}ActiveLabel2", fill="#48426D")
                        self.canvas.moveto(f"mwActive", 550, 428)
                function()

            self.canvas.tag_bind(f"{tag}Button", "<Button-1>", onClick)
            self.canvas.tag_bind(f"{tag}Button", "<ButtonRelease-1>", onRelease)

    def onRaise(self) -> None:
        log("Raised Summaries")

        self.canvas.delete("all")
        self.initImages()
        self.initUi()

        summarizer = SalesSummaries()
        currentUser = App.sellerScenes["SellerHome"]["account"]["username"]

        points = summarizer.getMonthlySales(
            currentUser,
            self.year,
            self.month,
        )
        highest = summarizer.getHighestValue(points)

        self.initGraphArea(
            f"This month's Sales   |   {calendar.month_name[self.month]} - {self.year}",
            "DAY",
            31,
            5,
            yHighest=highest,
            points=points
        )