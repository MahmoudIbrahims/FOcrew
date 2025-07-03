from enum import Enum

class Languages(Enum):
    ENGLISH ="English"
    ARABIC ="Arabic"


class FileNameEnum(Enum):
    CSV ="text/csv"
    EXCEL ="application/vnd.ms-excel"
    SHEET="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"