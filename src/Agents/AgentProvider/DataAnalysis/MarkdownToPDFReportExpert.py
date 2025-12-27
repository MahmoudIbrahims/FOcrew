from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.ConvertToPDF import MarkdownToPDFReport
from tools.run_command_tool import RunCommandTool

class ReportGeneratorAgent(BaseAgent):
    def __init__(self,cmd_tool: RunCommandTool):
        provider = ProviderLLM()
        llm = provider.get_llm()
        pdf_tool = MarkdownToPDFReport()

        super().__init__(
            name="Markdown Report Generator",
            role="Report Builder",
            goal="Generate clean PDF reports from Markdown with company logo.",
            backstory="\n".join([
                "You are responsible for transforming raw Markdown analysis files",
                "into professional PDF reports with tables, styling, and logos.",
                "Your reports are then passed to managers or other agents."
            ]),
            llm=llm,
            reasoning=True,
            allow_delegation=False,
            tools=[pdf_tool,cmd_tool],
        )

    def get_task(self):
        return Task(
            description="\n".join([
                "Take the Markdown analysis file (default: results/Data_Analysis/Analysis_Report.md).",
                "1. Use the `Markdown to PDF Report Generator` tool.",
                "2. Provide the correct logo path (../docs.logo.png).",
                "3. Save the generated PDF in $full_path.",
                "4. Confirm the PDF path in the output."
            ]),
            agent=self.get_agent(),
            context_keys=["Markdown_report_path"],
            expected_output="Final_generated_PDF_report"
        )
