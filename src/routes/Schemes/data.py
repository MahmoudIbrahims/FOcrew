from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id : str = None 
    do_reset : Optional[int] = 0
    