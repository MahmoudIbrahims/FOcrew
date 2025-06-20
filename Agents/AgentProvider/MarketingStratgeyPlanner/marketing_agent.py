from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM


class MarketingStrategist(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        super().__init__(
                    name ="Marketing Strategist",
                    role="Strategic Marketing Planner",
                    goal="Create comprehensive marketing plans and strategies",
                    backstory="Experienced marketing professional with expertise in campaign planning",
                    llm=llm
                     )
        
    def get_task(self):
        return Task(
            description="Create marketing plan based on the SWOT analysis results",
            agent=self.get_agent(),
            expected_output="Comprehensive marketing strategy"
        )
            

