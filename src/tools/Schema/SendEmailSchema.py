from pydantic import BaseModel
from typing import Optional

class WebhookSchema(BaseModel):
    result: str
    

class EmailSchema(BaseModel):
    to: str="mahmoudibrahimsalman@gmail.com"
    subject: Optional[str] = "Inventory Report"
    body: Optional[str] = "report Inventory management"
    pdf_path: Optional[str] = "results/inventory_management/report.pdf"