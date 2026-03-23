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
    PASSWORD_INVALID        = 4
    MISSING_USERNAME        = 5
    MISSING_PASSWORD        = 6
    MISSING_HER             = 7
    CART_EMPTY              = 8
    INSUFFICIENT_PAYMENT    = 9
    INSUFFICIENT_STOCK      = 10
    ITEM_NOT_FOUND          = 12