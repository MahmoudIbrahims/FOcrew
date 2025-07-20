from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.dashboard_tool import  ComprehensiveDashboardTool   #DashboardTool ComprehensiveDashboardTool
from ...Prompts import Visualization_description_prompt , Visualization_expected_output_prompt

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
        file_path = self.get_config().DATA_PATH  

        return Task(
            description=Visualization_description_prompt.safe_substitute(file_path=file_path),
            agent=self.get_agent(),
            expected_output=Visualization_expected_output_prompt.safe_substitute(file_path=file_path),
            output_file="results/Dashboard/Complete_Dashboard.html"
        )

            
            
                        



