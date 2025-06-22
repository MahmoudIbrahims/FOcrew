from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool 

class InventoryAnalysisReportingSpecialist(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        file_tool = FileTool()
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
                    tools=[file_tool]  
            
                     )
        
    def get_task(self):
        return Task(
            description="\n".join([
                "Create comprehensive inventory management reports and recommendations.",
                
                "Your responsibilities:",
                "1. Synthesize all previous analyses into a comprehensive report",
                "2. Generate critical alerts for immediate action items",
                "3. Create executive summary with key findings",
                "4. Provide specific recommendations for each inventory category",
                "5. Calculate key performance indicators (KPIs)",
                "6. Identify cost-saving opportunities",
                "7. Create action plan with priorities and timelines",
                
                "Include in your analysis:",
                " - Current inventory health status",
                "- Items requiring immediate attention",
                "- Medium and long-term recommendations",
                "- Financial impact assessment",
                "- Risk analysis",
    
                "Make the report clear and actionable for decision-makers."  
                
                             ]),
            agent=self.get_agent(),
            expected_output="\n".join([
                "Comprehensive inventory report including:",
                "- Executive summary with key findings",
                "- Critical alerts and immediate action items",
                "- Detailed recommendations by item category",
                "- KPI dashboard (inventory turnover, stockout risk, etc.)",
                "- Implementation roadmap with priorities",
                "- Risk assessment and mitigation strategies",
                    ]),
                )
            
            
            
            
            
        