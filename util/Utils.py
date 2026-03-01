import ctypes
import json
from enum import Enum

class Color(Enum):
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"

def log(log: object, tag: str = None) -> None:
    print(Color.GREEN.value, log, Color.RESET.value, sep="", end='')
    if tag is not None:
        print(f" {Color.YELLOW.value}|{Color.RESET.value} ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

def logbr() -> None:
    print("-" * 500)

def warn(warning: object, tag: str = None) -> None:
    print(Color.YELLOW.value, warning, Color.RESET.value, sep="", end="")
    if tag is not None:
        print(f" {Color.YELLOW.value}|{Color.RESET.value} ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

def wtf(wtf: object, tag: str = None) -> None:
    # WTF means "What a Terrible Failure"
    # nakuha ko lang nung nagawa ako ng app sa phone (Log.wtf("", ""))
    print(Color.RED.value, wtf, Color.RESET.value, sep="", end='')
    if tag is not None:
        print(f" {Color.YELLOW.value}|{Color.RESET.value} ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

def logData(data: object, tag: str=None) -> None:
    if tag:
        log(tag)

    print(json.dumps(data, indent=4))

def initFont(fontName: str) -> None:
    ctypes.windll.gdi32.AddFontResourceExW(f"res/fonts/{fontName}", 0x10, 0)