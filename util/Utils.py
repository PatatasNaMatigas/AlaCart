from enum import Enum

class Color(Enum):
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"

def coloredText(text: str, color: Color) -> str:
    return color.value + text + Color.RESET.value

def warn(warning: str) -> None:
    print(coloredText(warning, Color.YELLOW))

def wtf(wtf: str) -> None:
    # WTF means "What a Terrible Failure"
    # nakuha ko lang nung nagawa ako ng app sa phone (Log.wtf("", ""))
    print(coloredText(wtf, Color.RED))