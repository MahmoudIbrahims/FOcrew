from crewai import LLM
from helpers.config import get_settings
from Agents.AgentEnums import AgentName

class ProviderLLM:
    def __init__(self):
        self.enums = AgentName
        settings = get_settings()
        self.llm = LLM(
            model=settings.MODEL_NAME,
            api_key=settings.API_KEY,
        )
    
    def get_llm(self):
        return self.llm