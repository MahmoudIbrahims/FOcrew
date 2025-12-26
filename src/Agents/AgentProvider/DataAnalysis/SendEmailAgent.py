from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.SendEmail_tool import SendEmailTool

class ReportSenderAgent(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        Gmail_tool= SendEmailTool()

        super().__init__(
            name="Gmail Report Sender",
            role="Email Dispatcher",
            goal="Send generated reports to Gmail",
            backstory="\n".join([
                "You are responsible for delivering analysis results to stakeholders.",
                "You send the final reports automatically to using Gmail SMTP."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[Gmail_tool],
        )

    def get_task(self):
        return Task(
            description="\n".join([
                "Take the pdf analysis this file path $file_path.",
                "1. Use the `Send Report via Gmail` tool.",
                "2. Pass a suitable subject (like 'Inventory Report').",
                "3. Pass the report body pdf or text or summary.",
                "4. sent to $manager"
            ]),
            agent=self.get_agent(),
            context_keys=["Final_generated_PDF_report"],
            expected_output="Report successfully sent → Gmail"
        )
