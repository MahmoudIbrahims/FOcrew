from crewai import LLM
from.helpers.config import get_settings

class GeminiModel:
    def __init__(self, config):
        self.llm = LLM(
            model=get_settings.MODEL_NAME,
            api_key=get_settings.API_KEY,
        )
    
    def get_llm(self):
        return self.llm