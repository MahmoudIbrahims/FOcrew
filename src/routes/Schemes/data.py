from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    Language :    str =None 
    COMPANY_NAME: str =None
    INDUSTRY_NAME:str =None
    do_reset : Optional[int] = 0
    