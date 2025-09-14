from pydantic import BaseModel
from typing import Optional

class WebhookSchema(BaseModel):
    result: str
    

class EmailSchema(BaseModel):
    to: str="mostafaabddalla856@gmail.com"
    subject: Optional[str] = "Inventory Report"
    body: Optional[str] = "Hello manager this is report Inventory management"
    pdf_path: Optional[str] = "results/inventory_management/report.pdf"