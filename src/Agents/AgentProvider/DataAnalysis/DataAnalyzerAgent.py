from crewai import Agent,Task
from tools.run_command_tool import RunCommandTool
from Providers import ProviderLLM
from ..BaseAgent import BaseAgent

class DataAnalyzerAgent(BaseAgent):
    def __init__(self):
        llm = ProviderLLM().get_llm()
        cmd_tool = RunCommandTool()

        super().__init__(
            name="DataAnalyzerAgent",
            role="Data Analyst",
            goal="Perform statistical analysis and extract key insights.",
            backstory="Analyst specialized in numeric feature evaluation and trend discovery.",
            llm=llm,
            tools=[cmd_tool],
        )

    def get_task(self):
           return Task(
                description=(
                    "Perform an in-depth analysis on the cleaned dataset.\n\n"
                    "Steps:\n"
                    "1. Generate Python code for statistical summaries and feature correlations.\n"
                    "2. Execute code to compute metrics (mean, std, skew, etc.).\n"
                    "3. Identify key trends, anomalies, or interesting relationships.\n"
                    "4. Return analytical insights for the visualization stage."
                ),
                expected_output="Key statistical summaries and detected data trends.",
                agent=self.get_agent(),
                context_keys=["cleaned_data_summary"],
                output_key="analysis_summary"
            )

