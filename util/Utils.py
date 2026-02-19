from enum import Enum

class Color(Enum):
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"

def log(log: object) -> None:
    print(Color.GREEN.value, log, Color.RESET.value)

def logbr() -> None:
    print("-" * 500)

def warn(warning: object) -> None:
    print(Color.YELLOW.value, warning, Color.RESET.value)

def wtf(wtf: object) -> None:
    # WTF means "What a Terrible Failure"
    # nakuha ko lang nung nagawa ako ng app sa phone (Log.wtf("", ""))
    print(Color.RED.value, wtf, Color.RESET.value)