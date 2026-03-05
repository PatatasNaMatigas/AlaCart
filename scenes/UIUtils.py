import tkinter as tk

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