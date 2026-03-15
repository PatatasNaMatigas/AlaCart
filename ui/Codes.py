from enum import Enum

class ThreatLevel(Enum):
    NONE      = 0
    LOW       = 1
    MODERATE  = 2
    HIGH      = 3
    CRITICAL  = 4
    DKN_MAHAL = 5

class ReturnCode(Enum):
    SUCCESS                 = 0
    ACCOUNT_DOES_NOT_EXIST  = 1
    ACCOUNT_ALREADY_EXISTS  = 2
    PASSWORD_INCORRECT      = 3
    PASSWORD_INVALID        = 3
    MISSING_USERNAME        = 4
    MISSING_PASSWORD        = 5
    MISSING_HER             = 6