from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.dashboard_tool import  ComprehensiveDashboardTool   #DashboardTool ComprehensiveDashboardTool


class DataVisualizationExpert(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        Plotly_DashboardTool =ComprehensiveDashboardTool()
        super().__init__(
                        name="Data Visualization Expert",
                        role="Data Visualization Expert",
                        goal="Create interactive dashboards and visual reports from inventory data",
                        backstory="You are an expert in data visualization who transforms complex inventory analytics into clear, interactive visual reports that help managers make quick decisions.",
                        llm=llm,
                        allow_delegation=False,
                        tools=[Plotly_DashboardTool]
                             )
    def get_task(self):
        return Task(
            description="".join([
                "1. Create an interactive inventory dashboard and visual reports using your dashboard tools. ",
                "2. Generate comprehensive charts, KPIs, and actionable insights from the inventory data. ",
                "3. 📁 CRITICAL: Save your complete dashboard as an HTML file to 'results/Dashboard/Complete_Dashboard.html'. ",
                "4. Ensure the directory structure exists and the file is properly saved. ",
                "5. Include interactive elements like filters, hover effects, and drill-down capabilities. ",
                "6. Confirm successful file creation before completing the task."
            ]),
            agent=self.get_agent(),
            expected_output="Interactive HTML dashboard saved to results/Dashboard/Complete_Dashboard.html with confirmation of successful file creation",
        )
               
            
            
            
                        



