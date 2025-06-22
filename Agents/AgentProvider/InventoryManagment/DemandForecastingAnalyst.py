from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM


class DemandForecastingAnalyst(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        
        super().__init__(
                    name="Demand Forecasting Analyst",
                    role="Demand Forecasting Analyst",
                    goal="Predict future demand patterns and analyze historical trends",
                    backstory="\n".join([
                        "You are a forecasting expert who specializes in analyzing historical sales data to predict future demand.",
                        "You use statistical methods and pattern recognition to provide accurate demand forecasts."
                        ]),
                    llm=llm,
                    allow_delegation=False
                     )
        
    
    def get_task(self):
        return Task(
            description="Analyze sales data and create demand forecasts",
            agent=self.get_agent(),
            expected_output="Weekly/monthly forecasts with trend analysis and stock coverage"
        )