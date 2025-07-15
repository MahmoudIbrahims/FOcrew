from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.FileReading import FileTool,DirectoryTool,BatchFileReader


class DataProcessing(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        file_tool = FileTool()
        directory_tool =DirectoryTool()
        batch_file_reader =BatchFileReader()
        super().__init__(
                    name="Data Processing Specialist",
                    role="Data Processing Specialist",
                    goal="Process and analyze inventory data files efficiently regardless of size",
                    backstory="\n".join([
                        "You are a data processing expert who specializes in handling various file formats and sizes."
                        "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
                        ]),
                    llm=llm,
                    allow_delegation=False,
                    tools=[file_tool], 
                    reasoning=True,  # Enable reasoning
                    max_reasoning_attempts=5  # Optional: Set a maximum number of reasoning attempts
                    )
            
                     
    def get_task(self):
        return Task(
            description="Analyze inventory data and prepare for analysis",
            agent=self.get_agent(),
            expected_output="results/inventory_management/DataProcessing_report.md"
            #"Complete data summary with basic statistics"
                 )