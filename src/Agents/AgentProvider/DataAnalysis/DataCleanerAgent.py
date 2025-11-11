from crewai import Agent,Task
from tools.run_command_tool import RunCommandTool
from Providers import ProviderLLM
from ..BaseAgent import BaseAgent

class DataCleanerAgent(BaseAgent):
    def __init__(self):
        llm = ProviderLLM().get_llm()
        cmd_tool = RunCommandTool()

        super().__init__(
            name="DataCleanerAgent",
            role="Data Cleaner",
            goal="Generate Python code to clean and preprocess the dataset.",
            backstory="Expert in handling missing values, outliers, and data types.",
            llm=llm,
            tools=[cmd_tool],
        )

    def get_task(self):
           return Task(
                description=(
                    "Clean and preprocess the dataset based on the summary provided by the Data Reader.\n\n"
                    "Steps:\n"
                    "1. Identify missing values, inconsistent data types, or outliers.\n"
                    "2. Generate Python code to clean the dataset.\n"
                    "3. Execute that code using the RunCommandTool.\n"
                    "4. Return a cleaned dataset summary and actions performed."
                ),
                expected_output="A clean dataset summary and code execution log showing preprocessing steps.",
                agent=self.get_agent(),
                context_keys=["dataset_summary"],
                output_key="cleaned_data_summary"
            )
