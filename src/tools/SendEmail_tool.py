import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type
from helpers.config import get_settings
from .Schema.SendEmailSchema import EmailSchema,Body_template
from email.utils import formataddr
import os


class SendEmailTool(BaseTool):
    name: str = "Send Report via Gmail"
    description: str = "Send CrewAI results + optional PDF directly via Gmail SMTP"
    args_schema: Type[BaseModel] = EmailSchema

    def _run(self, to: str, 
             subject: str = "Inventory Report by FOcrew", 
             body : str ="hello manager",
             pdf_path: str = "results/inventory_management/report.pdf") -> str:
        
        settings = get_settings()
        sender = settings.GMAIL_USER      
        password = settings.GMAIL_APP_PASSWORD
    
        msg = MIMEMultipart()
        msg['From'] = formataddr(("FOcrew Team", sender))
        msg['To'] = to
        msg['Subject'] = subject
        body = Body_template.safe_substitute()   
        msg.attach(MIMEText(body, 'plain'))

        # PDF
        if pdf_path:
            with open(pdf_path, "rb") as f:
                mime = MIMEBase("application", "pdf")
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                filename = os.path.basename(pdf_path)
                mime.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(mime)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            return f"Email sent successfully to {to}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

