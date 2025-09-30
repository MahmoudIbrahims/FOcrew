from pydantic import BaseModel
from typing import Optional
from string import Template

class WebhookSchema(BaseModel):
    result: str
    

class EmailSchema(BaseModel):
    to: str="mahmoudibrahimsalman@gmail.com"
    subject: Optional[str] = "Inventory Report"
    body: Optional[str] = "report Inventory management"
    pdf_path: Optional[str] = "results/inventory_management/report.pdf"
    


Body_template =Template("\n".join([
                "Dear manager",
                
                "I hope this email finds you well.",
                "The inventory analysis has been successfully completed.",
                "Please find attached a detailed PDF report.",
                "This report is intended to support decision-making and enhance overall warehouse efficiency.",

                "Best regards",
                "FOcrew Team"
     
                                  ]))     