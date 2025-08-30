import requests
from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type
from helpers.config import get_settings
from .Schema import WebhookSchema


class WebhookTool(BaseTool):
    name :str = "Send Results to Zapier"
    description:str = "Send CrewAI results to a Zapier Webhook for Gmail forwarding"
    args_schema : Type[BaseModel]=WebhookSchema

    def _run(self, result: dict) -> dict:
        setting =get_settings()
        webhook_url = setting.webhook_url
        payload = {"result": result}
        response = requests.post(webhook_url, json=payload)
        return f"Sent to Zapier with status {response.status_code}"
