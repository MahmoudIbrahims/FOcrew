from crewai import Agent,Task
from tools.markdown_tool import MarkdownTool
from Providers import ProviderLLM
from ..BaseAgent import BaseAgent

class ReportWriterAgent(BaseAgent):
    def __init__(self):
        llm = ProviderLLM().get_llm()
        md_tool = MarkdownTool()

        super().__init__(
            name="ReportWriterAgent",
            role="Business Report Writer",
            goal="Write a concise, insightful business report summarizing findings.",
            backstory="Transforms technical data insights into executive-level business recommendations.",
            llm=llm,
            reasoning=True,
            tools=[md_tool],
        )

    def get_task(self):
            return Task(
                description=(
                    "Write a professional business-focused Markdown report summarizing all findings.\n\n"
                    "Steps:\n"
                    "1. Combine data summaries, analysis, and visual insights.\n"
                    "2. Write an executive-style report highlighting key insights, trends, and recommendations.\n"
                    "3. Save the report to results/Data_Analysis/Analysis_Report.md using MarkdownTool."
                ),
                expected_output="A clear and well-structured Markdown report containing insights and recommendations.",
                agent=self.get_agent(),
                context_keys=["dataset_summary", "cleaned_data_summary", "analysis_summary", "visualization_summary"],
                output_key="final_report_path"
            )