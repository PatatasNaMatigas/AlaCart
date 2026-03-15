import ctypes
import json
from enum import Enum

class Colors(Enum):
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"

class Fonts(Enum):
    KOULEN = "koulen"
    MONO_MANIAC = "monomaniac one regular"

def log(log: object, tag: str = None) -> None:
    if not log:
        return
    print(Colors.GREEN.value, log, Colors.RESET.value, sep="", end='')
    if tag is not None:
        print(f" {Colors.YELLOW.value}|{Colors.RESET.value} ", Colors.BLUE.value, tag, Colors.RESET.value, sep="")
    else:
        print()

def logbr() -> None:
    print("-" * 500)

def warn(warning: object, tag: str = None) -> None:
    if not warning:
        return
    print(Colors.YELLOW.value, warning, Colors.RESET.value, sep="", end="")
    if tag is not None:
        print(f" {Colors.YELLOW.value}|{Colors.RESET.value} ", Colors.BLUE.value, tag, Colors.RESET.value, sep="")
    else:
        print()

def wtf(wtf: object, tag: str = None) -> None:
    # WTF means "What a Terrible Failure"
    # nakuha ko lang nung nagawa ako ng app sa phone (Log.wtf("", ""))
    if not wtf:
        return
    print(Colors.RED.value, wtf, Colors.RESET.value, sep="", end='')
    if tag is not None:
        print(f" {Colors.YELLOW.value}|{Colors.RESET.value} ", Colors.BLUE.value, tag, Colors.RESET.value, sep="")
    else:
        print()

def logData(data: object, tag: str=None) -> None:
    if not data:
        return
    if tag:
        log(tag)

    print(json.dumps(data, indent=4))

def initFont(fontName: str) -> None:
    ctypes.windll.gdi32.AddFontResourceExW(f"../res/fonts/{fontName}", 0x10, 0)