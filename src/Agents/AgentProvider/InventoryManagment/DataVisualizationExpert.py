from crewai import Task
from ..BaseAgent import BaseAgent
from Providers.ProviderLLM import ProviderLLM
from tools.VisualizationTool import PlotlyDashboardTool,ReportGeneratorTool

class DataVisualizationExpert(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        Plotly_DashboardTool =PlotlyDashboardTool()
        Report_GeneratorTool = ReportGeneratorTool()
        super().__init__(
                        name="Data Visualization Expert",
                        role="Data Visualization Expert",
                        goal="Create interactive dashboards and visual reports from inventory data",
                        backstory="You are an expert in data visualization who transforms complex inventory analytics into clear, interactive visual reports that help managers make quick decisions.",
                        llm=llm,
                        allow_delegation=False,
                        tools=[Plotly_DashboardTool,Report_GeneratorTool]
                             )
    def get_task(self):
        return Task(
            description="Create interactive inventory dashboard and visual reports",
            agent=self.get_agent(),
            expected_output="Interactive HTML dashboard with charts, KPIs, and actionable insights"
        )
                
            
            
            
                        



