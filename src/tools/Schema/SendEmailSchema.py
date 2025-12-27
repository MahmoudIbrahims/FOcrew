from pydantic import BaseModel
from typing import Optional
from string import Template

class WebhookSchema(BaseModel):
    result: str
    

class EmailSchema(BaseModel):
    to: str="mahmoudibrahimsalman@gmail.com"
    subject: Optional[str] = "Analysis Report"
    body: Optional[str] = "Report Analysis management"
    pdf_path: Optional[str] = "results/inventory_management/report.pdf"
    


Body_template =Template("\n".join([
                "Dear manager",
                
                "I hope this email finds you well.",
                "The analysis has been successfully completed.",
                "Please find attached a detailed PDF report.",
                "This report is intended to support decision-making and enhance overall efficiency.",

                "Best regards",
                "FOcrew Team"
     
                                  ]))     