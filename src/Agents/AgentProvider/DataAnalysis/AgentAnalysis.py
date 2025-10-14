# from crewai import Task
# from ..BaseAgent import BaseAgent
# from Providers import ProviderLLM
# from tools.JupyterNodebook import LiveJupyterKernelTool
# from tools.LiveNotebookTool import WindowNotebookTool
# import os

# class DataAnalysisAgent(BaseAgent):
#     def __init__(self):
#         provider = ProviderLLM()
#         llm = provider.get_llm()
#         jupyter_tool = LiveJupyterKernelTool()
#         Window_NotebookTool=WindowNotebookTool()

#         super().__init__(
#             name="Data Analysis Executor",
#             role="Data Analysis and Execution Specialist",
#             goal="Analyze uploaded dataset files dynamically by generating Python code and executing it live in a Jupyter kernel.",
#             backstory="\n".join([
#                 "You are an AI data analyst specialized in understanding and analyzing structured data files (CSV, Excel, JSON).",
#                 "You can generate Python code for data cleaning, exploration, and visualization.",
#                 "You can execute your code live using the Jupyter tool to show results in real-time.",
#                 "You are methodical — always reason step-by-step and handle large datasets efficiently."
#             ]),
#             llm=llm,
#             allow_delegation=False,
#             tools=[jupyter_tool,Window_NotebookTool],
#         )

#     def get_task(self):   #, metadata: dict = None):
#         # """
#         # file_path: المسار الكامل للملف المحفوظ على السيرفر
#         # metadata: بيانات إضافية (زي نوع الملف، اسم المستخدم، تاريخ الرفع...)
#         # """
#         # file_name = os.path.basename(file_path)
#         # #meta_info = f"\nFile Metadata:\n{metadata}\n" if metadata else ""

#         return Task(
#             description="\n".join([
#                 f"You have been provided with a dataset file located at: $file_path.",
#                 "Your mission is to:",
#                 "* Use the tool `WindowNotebookTool` to open an interactive window that simulates a Jupyter Notebook.",
#                 "* use the tool `LiveJupyterKernelTool` to open jupyter nodebook to run the code.*"
#                 "1. Load the dataset using Python (pandas).",
#                 "2. Analyze its structure (columns, nulls, types).",
#                 "3. Perform exploratory data analysis (EDA).",
#                 "4. Generate visualizations (if useful).",
#                 "5. Identify potential issues or anomalies.",
#                 "6. Provide actionable insights.",
#                 "7. Generate Python code for each step and execute it live using your Jupyter tool.",
#                 "8. Make sure every step’s output (dataframe head, charts, summaries) is shown in real time.",
#                 "9. Save your final markdown analysis report to: `results/inventory_management/Analysis_Report.md`.",
#                 # f"File to analyze: **{file_name}**",
#                 # meta_info,
#                 "---",
#                 "💡 Use your Live Jupyter Kernel Executor tool to run all generated Python code blocks and collect results."
#             ]),
#             agent=self.get_agent(),
#             expected_output="A complete markdown analysis report of the dataset with results and visuals.",
#             output_key="analysis_report_path"
#         )

#================================================
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
                "You have been provided with a dataset file located at: `$file_path`.",
                "",
                "🎯 **Your mission:**",
                "1. Load and inspect the dataset using Python (pandas).",
                "2. Analyze structure (columns, nulls, data types).",
                "3. Perform exploratory data analysis (EDA).",
                "4. Create visualizations (if relevant).",
                "5. Identify issues or anomalies and describe insights.",
                "",
                "---",
                "🧠 **Error Handling Protocol:**",
                "- If any error occurs while running code in the Jupyter tool:",
                "  * Read and interpret the traceback carefully.",
                "  * Diagnose the exact cause (e.g., missing column, NaN issue, wrong variable name, plotting error).",
                "  * Correct the code step-by-step.",
                "  * Re-run the corrected version automatically until successful.",
                "  * Document the correction you made (what failed, why, and how you fixed it).",
                "",
                "---",
                "💡 **Tools to Use:**",
                "* Use `WindowNotebookTool` to display your live notebook interface.",
                "* Use `LiveJupyterKernelTool` to execute your Python code and visualize results.",
                "",
                "---",
                "📦 **Final Deliverable:**",
                "Generate a well-formatted markdown analysis report containing:",
                "- Dataset summary and key metrics",
                "- Data issues or inconsistencies",
                "- Graphs and descriptive statistics",
                "- Insights and business recommendations",
                "",
                "Save your final report to: `results/inventory_management/Analysis_Report.md`"
            ]),
            agent=self.get_agent(),
            expected_output="A complete markdown analysis report of the dataset with results, charts, and professional explanations.",
            output_key="analysis_report_path"
        )
