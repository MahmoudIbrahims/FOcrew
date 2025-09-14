# import requests
# from crewai.tools import BaseTool
# from pydantic import BaseModel
# from typing import Type
# from helpers.config import get_settings
# from .Schema import WebhookSchema


# class WebhookTool(BaseTool):
#     name: str = "Send Report to Zapier"
#     description:str = "Send CrewAI results to a Zapier Webhook for Gmail forwarding"
#     args_schema : Type[BaseModel]=WebhookSchema

#     def _run(self, result: dict) -> dict:
#         setting =get_settings()
#         webhook_url = setting.webhook_url
#         payload = {"result": result}
#         response = requests.post(webhook_url, json=payload)
#         return f"Sent to Zapier with status {response.status_code}"
#==========================================================================

# import requests
# from crewai.tools import BaseTool
# from pydantic import BaseModel
# from typing import Optional,Type
# from helpers.config import get_settings

# class WebhookSchema(BaseModel):
#     result: dict
#     subject: Optional[str] = "Inventory Report"
#     pdf_path: Optional[str] = None


# class WebhookTool(BaseTool):
#     name: str = "Send Report to Zapier"  
#     description: str = "Send CrewAI results + optional PDF to a Zapier Webhook for Gmail forwarding"
#     args_schema : Type[BaseModel]=WebhookSchema

#     def _run(self, result: dict, subject: str = "Inventory Report", pdf_path: str = None) -> dict:
#         setting = get_settings()
#         webhook_url = setting.webhook_url

#         payload = {"result": result, "subject": subject}
#         files = {"file": open(pdf_path, "rb")} if pdf_path else None

#         response = requests.post(webhook_url, data=payload, files=files)

#         if files:
#             files["file"].close()

#         return f"Sent to Zapier with status {response.status_code}"
# ======================

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type
from helpers.config import get_settings
from .Schema.SendEmailSchema import EmailSchema

class SendEmailTool(BaseTool):
    name: str = "Send Report via Gmail"
    description: str = "Send CrewAI results + optional PDF directly via Gmail SMTP"
    args_schema: Type[BaseModel] = EmailSchema

    def _run(self, to: str ="mostafaabddalla856@gmail.com", 
             subject: str = "Inventory Report by FOcrew", 
             body: str = """
             Dear manager 
             I hope this email finds you well .,
             The inventory analysis has been successfully completed.,
             please find attached a detailed PDF report .,
             
             This report is intended to support decision-Making and enhance overall warehouse efficiency.
             
             Best regards:
             FOcrew Team 
             """,
             pdf_path: str = "results/inventory_management/report.pdf") -> str:
        
        settings = get_settings()
        sender = settings.GMAIL_USER      
        password = settings.GMAIL_APP_PASSWORD 

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # PDF
        if pdf_path:
            with open(pdf_path, "rb") as f:
                mime = MIMEBase("application", "pdf")
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                mime.add_header("Content-Disposition", f"attachment; filename={pdf_path}")
                msg.attach(mime)

        # SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())
        server.quit()

        return f"Email sent successfully to {to}"
