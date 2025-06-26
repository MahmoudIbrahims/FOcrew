from crewai import Task
from ..BaseAgent import BaseAgent
from Providers.ProviderLLM import ProviderLLM

class ContentPlanner(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        super().__init__(
            name="Content planner",
            role="Responsible for creating engaging content",
            goal="Plan and strategize content for marketing campaigns",
            backstory="Creative content strategist with expertise in multi-channel content planning",
            llm=llm
            
              )
        
    def get_task(self):
        return Task(
            description="Plan content strategy for the marketing campaign",
            agent=self.get_agent(),
            expected_output="Content calendar and strategy"
        )
        