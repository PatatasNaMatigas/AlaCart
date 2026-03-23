import datetime
import calendar
import os
from dataManager import FileHandler as FH
from dataManager.FileHandler import DB_BASE


class SalesSummaries:
    def __init__(self):
        self.basePath = os.path.join(DB_BASE, "summaries")

    def getWeeklySales(self, owner: str, year: int = None, weekNumber: int = None) -> list[int]:
        today = datetime.date.today()
        year = year if year is not None else today.year
        weekNumber = weekNumber if weekNumber is not None else today.isocalendar()[1]

        weeklyPoints = []
        for dayIndex in range(1, 8):
            try:
                targetDate = datetime.date.fromisocalendar(year, weekNumber, dayIndex)
                weeklyPoints.append(int(self.__getDailyTotal(targetDate, owner)))
            except ValueError:
                weeklyPoints.append(0)

        return weeklyPoints

    def getMonthlySales(self, owner: str, year: int = None, month: int = None) -> list[int]:
        today = datetime.date.today()
        year = year if year is not None else today.year
        month = month if month is not None else today.month

        _, lastDay = calendar.monthrange(year, month)

        monthlyPoints = []
        for day in range(1, lastDay + 1):
            targetDate = datetime.date(year, month, day)
            monthlyPoints.append(int(self.__getDailyTotal(targetDate, owner)))

        return monthlyPoints

    def __getDailyTotal(self, date: datetime.date, owner: str) -> float:
        filePath = f"{self.basePath}/{date.year}/{date.month}/{date.day}/transactions.json"

        if not os.path.exists(filePath):
            return 0.0

        try:
            transactions = FH.read(filePath)
            sellerTotal = 0.0

            for transaction in transactions:
                items = transaction.get("items_summary", [])
                sellerTotal += sum(
                    item.get("sub_total", 0)
                    for item in items
                    if item.get("owner") == owner
                )
            return sellerTotal
        except Exception:
            return 0.0

    def getHighestValue(self, points: list[int]) -> int:
        if not points: return 100
        maxVal = max(points)
        return int(maxVal * 1.2) if maxVal > 0 else 100