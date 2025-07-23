from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.FileReading import BatchFileReader
from tools.Analysis_tool import InventoryAnalysisTool
from ...Prompts.DataِAnalysisPrompt import Analysis_description_prompt


class DataAnalysisSpecialist(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        batch_file_reader =BatchFileReader()
        Inventory_AnalysisTool =InventoryAnalysisTool()
        super().__init__(
                    name="Data Analysis Specialist",
                    role="Data Analysis Specialist",
                    goal="Process and analyze inventory data files efficiently regardless of size",
                    backstory="\n".join([
                                "You are a highly skilled data processing expert specializing in inventory data.",
                                "You can efficiently handle large CSV or Excel files, clean inconsistencies, and generate professional summaries in markdown format.",
                                "You never fabricate data and only rely on what's present in the uploaded file."
                         ]),
                     
                    llm=llm,
                    allow_delegation=False,
                    tools=[batch_file_reader], 
                    reasoning=True,  # Enable reasoning
                    max_reasoning_attempts=2  # Optional: Set a maximum number of reasoning attempts
                    )
        
    def get_task(self):
        return Task(
                description=Analysis_description_prompt.template,
                agent=self.get_agent(),
                expected_output="A comprehensive Markdown report with tables summarizing the real inventory data analysis.",
                output_file="results/inventory_management//DataAnalysis_Report.md"
        )

            
   