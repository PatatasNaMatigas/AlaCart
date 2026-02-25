from enum import Enum

class Color(Enum):
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    RESET  = "\033[0m"

def log(log: object, tag: str = None) -> None:
    print(Color.GREEN.value, log, Color.RESET.value)
    if tag is not None:
        print(" | ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

def logbr() -> None:
    print("-" * 500)

def warn(warning: object, tag: str = None) -> None:
    print(Color.YELLOW.value, warning, Color.RESET.value, sep="", end="")
    if tag is not None:
        print(" | ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

def wtf(wtf: object, tag: str = None) -> None:
    # WTF means "What a Terrible Failure"
    # nakuha ko lang nung nagawa ako ng app sa phone (Log.wtf("", ""))
    print(Color.RED.value, wtf, Color.RESET.value)
    if tag is not None:
        print(" | ", Color.BLUE.value, tag, Color.RESET.value, sep="")
    else:
        print()

openDelimiters = [
    '[', '{', '('
]
closeDelimiters = [
    ']', '}', ')'
]
def logData(data: object, tag: str = None) -> None:
    if tag is not None:
        print(Color.BLUE.value, tag, Color.RESET.value, sep="")
    depth = 0
    previousChar = ''
    for char in str(data):
        print(
            (depth * 5)  * " "
                if previousChar not in openDelimiters
                or previousChar not in closeDelimiters
                or previousChar != ','
                or previousChar != '\''
                else "",
            char,
            end=''
        )
        if char in openDelimiters:
            print()
            depth += 1
        elif char in closeDelimiters:
            print()
            depth -= 1
        elif char == ',':
            print()
        previousChar = char