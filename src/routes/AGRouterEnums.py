from enum import Enum

class Languages(Enum):
    ENGLISH ="English"
    ARABIC ="Arabic"


class FileNameEnum(Enum):
    CSV = "csv"
    EXCEL = "xlsx"
    SHEET = "xls"