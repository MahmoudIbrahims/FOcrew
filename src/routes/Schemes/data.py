from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    Language :    str =None 
    COMPANY_NAME: str =None
    INDUSTRY_NAME:str =None
    MANAGER_EMAIL:str =None
    do_reset : Optional[int] = 0


class DataAnaltsisRequest(BaseModel):
    Language:str =None
    
    
    