from enum import Enum

class Languages(Enum):
    ENGLISH ="English"
    ARABIC ="Arabic"


class FileNameEnum(Enum):
    CSV   = "csv"
    EXCEL = "xlsx"
    SHEET = "xls"
    

class UsageType(Enum):
    INPUT ="input"
    OUTPUT ="output"
    Reference ="reference"