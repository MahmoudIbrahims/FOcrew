from crewai import Task
from ..BaseAgent import BaseAgent
from Providers.ProviderLLM import ProviderLLM

class SWOTAnalyst(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        super().__init__(
                    name="SWOT Analyst",
                    role="Strategic Business Analyst",
                    goal="Analyze company strengths, weaknesses, opportunities, and threats",
                    backstory="Expert business analyst specializing in strategic analysis",
                    llm=llm
                )
            
    def get_task(self):
        return Task(
            description=f"Analyze {self.get_config().COMPANY_NAME} in {self.get_config().INDUSTRY_NAME} industry. Provide SWOT analysis with strengths, weaknesses, opportunities, and threats.",
            agent=self.get_agent(),
            expected_output="Detailed SWOT analysis report"
                )