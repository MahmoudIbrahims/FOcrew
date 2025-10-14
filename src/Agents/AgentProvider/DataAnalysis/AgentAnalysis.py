from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.JupyterNodebook import LiveJupyterKernelTool
from tools.LiveNotebookTool import WindowNotebookTool
import os

class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        jupyter_tool = LiveJupyterKernelTool()
        window_tool = WindowNotebookTool()

        super().__init__(
            name="Data Analysis Executor",
            role="Data Analysis and Execution Specialist",
            goal="Analyze uploaded dataset files dynamically by generating Python code and executing it live in a Jupyter kernel.",
            backstory="\n".join([
                "You are an AI data analyst specialized in structured data (CSV, Excel, JSON).",
                "You can generate Python code for data cleaning, exploration, and visualization.",
                "You can execute your code live using the Jupyter tool to show results in real-time.",
                "You are analytical and systematic — always reason step-by-step, handle errors gracefully, and document your reasoning.",
                "If an error occurs, you immediately analyze the traceback, identify the root cause, fix the issue, and rerun the corrected code."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[jupyter_tool, window_tool],
        )

    def get_task(self):
        return Task(
            description="\n".join([
                    "Analyze the uploaded dataset file: $file_path",
                    "",
                    "Use the tool `Live Jupyter Notebook (Web)` to show a live Python execution window (like Jupyter Notebook).",
                    "Use the `Live Jupyter Kernel Executor` tool to run each Python step.",
                    "",
                    "Steps:",
                    "1. Load the dataset using pandas.",
                    "2. Explore columns, data types, and missing values.",
                    "3. Clean the data if needed.",
                    "4. Generate summary statistics and visualizations.",
                    "5. Find trends or anomalies.",
                    "6. Combine all results into a final Markdown report.",
                    "",
                    "Save the final report to: results/inventory_management/Analysis_Report.md",
                    ""
            ]),
            agent=self.get_agent(),
            expected_output="A complete markdown analysis report of the dataset with results, charts, and professional explanations.",
            output_key="analysis_report_path"
        )
