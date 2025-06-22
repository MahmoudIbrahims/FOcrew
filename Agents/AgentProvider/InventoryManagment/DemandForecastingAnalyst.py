from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool 


class DemandForecastingAnalyst(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        file_tool = FileTool()
        super().__init__(
                    name="Demand Forecasting Analyst",
                    role="Demand Forecasting Analyst",
                    goal="Predict future demand patterns and analyze historical trends",
                    backstory="\n".join([
                        "You are a forecasting expert who specializes in analyzing historical sales data to predict future demand.",
                        "You use statistical methods and pattern recognition to provide accurate demand forecasts."
                        ]),
                    llm=llm,
                    allow_delegation=False,
                    tools=[file_tool] 
            
                     )
        
    
    def get_task(self):
        return Task(
            description="\n".join([
                "Analyze historical sales data and create demand forecasts.",
                
                "Your responsibilities:",
                "1. Analyze historical sales patterns and trends",
                "2. Identify seasonal patterns if any",
                "3. Calculate demand forecasts for next week and month",
                "4. Determine demand variability and volatility",
                "5. Calculate stock coverage days for each item",
                "6. Identify fast-moving vs slow-moving items",
                
                "Use the processed data to generate forecasts using:",
                "- Moving averages",
                "- Trend analysis",
                "- Seasonal adjustments where applicable",
    
                "Focus on accuracy and practical applicability."  
                
                             ]),
            agent=self.get_agent(),
            expected_output="\n".join([
                "Demand forecasts including:",
                "- Weekly and monthly demand predictions for each item",
                "- Demand trend analysis (increasing/decreasing/stable)",
                "- Stock coverage analysis (days of inventory remaining)",
                "- Classification of items by demand velocity",
                "- Forecast accuracy indicators"
                    ]),
                )
            
            
            
            
            