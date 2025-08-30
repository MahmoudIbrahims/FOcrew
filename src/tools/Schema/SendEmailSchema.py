from pydantic import BaseModel

class WebhookSchema(BaseModel):
    result: str