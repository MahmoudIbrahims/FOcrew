from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool 

class InventoryAnalysisReportingSpecialist(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        #file_tool = FileTool()
        super().__init__(
                    name="Inventory Analysis & Reporting Specialist",
                    role="Inventory Analysis & Reporting Specialist",
                    goal="Generate comprehensive reports and actionable insights for inventory management",
                    backstory="\n".join([
                        "You are an inventory analyst who specializes in creating comprehensive reports and dashboards.",
                        "You synthesize all analysis results into clear, actionable insights for inventory managers and executives."
                        ]),
                    llm=llm,
                    allow_delegation=False,
                    #tools=[file_tool]  
            
                     )
        
    def get_task(self):
        return Task(
                description="Create comprehensive inventory management reports and recommendations",
                agent=self.get_agent(),
                expected_output="Executive summary, critical alerts, KPIs, and action plan"
            )
                    
            
            
        