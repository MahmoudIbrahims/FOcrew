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
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Optional,Type
from helpers.config import get_settings

class WebhookSchema(BaseModel):
    result: dict
    subject: Optional[str] = "Inventory Report"
    pdf_path: Optional[str] = None


class WebhookTool(BaseTool):
    name: str = "Send Report to Zapier"  
    description: str = "Send CrewAI results + optional PDF to a Zapier Webhook for Gmail forwarding"
    args_schema : Type[BaseModel]=WebhookSchema

    def _run(self, result: dict, subject: str = "Inventory Report", pdf_path: str = None) -> dict:
        setting = get_settings()
        webhook_url = setting.webhook_url

        payload = {"result": result, "subject": subject}
        files = {"file": open(pdf_path, "rb")} if pdf_path else None

        response = requests.post(webhook_url, data=payload, files=files)

        if files:
            files["file"].close()

        return f"Sent to Zapier with status {response.status_code}"
#======================

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from crewai.tools import BaseTool
# from pydantic import BaseModel
# from typing import Optional, Type
# from helpers.config import get_settings


# class EmailSchema(BaseModel):
#     to: str
#     subject: Optional[str] = "Inventory Report"
#     body: Optional[str] = "مرحباً، التقرير الجديد من Inventory management جاهز."
#     pdf_path: Optional[str] = None


# class SendEmailTool(BaseTool):
#     name: str = "Send Report via Gmail"
#     description: str = "Send CrewAI results + optional PDF directly via Gmail SMTP"
#     args_schema: Type[BaseModel] = EmailSchema

#     def _run(self, to: str, subject: str = "Inventory Report", body: str = "", pdf_path: str = None) -> str:
#         settings = get_settings()
#         sender = settings.gmail_user          # حط الإيميل في settings
#         password = settings.gmail_app_password  # App Password من جوجل

#         # إعداد الرسالة
#         msg = MIMEMultipart()
#         msg['From'] = sender
#         msg['To'] = to
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         # مرفق PDF
#         if pdf_path:
#             with open(pdf_path, "rb") as f:
#                 mime = MIMEBase("application", "pdf")
#                 mime.set_payload(f.read())
#                 encoders.encode_base64(mime)
#                 mime.add_header("Content-Disposition", f"attachment; filename={pdf_path}")
#                 msg.attach(mime)

#         # إرسال عبر SMTP
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(sender, password)
#         server.sendmail(sender, to, msg.as_string())
#         server.quit()

#         return f"Email sent successfully to {to}"
