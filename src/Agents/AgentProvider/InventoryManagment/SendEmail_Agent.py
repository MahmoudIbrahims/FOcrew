from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.SendEmail_tool import WebhookTool

class ReportSenderAgent(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        zapier_tool = WebhookTool()

        super().__init__(
            name="Zapier Report Sender",
            role="Email Dispatcher",
            goal="Send generated reports to managers via Gmail (through Zapier Webhook)",
            backstory="\n".join([
                "You are responsible for delivering analysis results to stakeholders.",
                "You send the final reports automatically to managers using Gmail through Zapier integration."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[zapier_tool],
        )

    def get_task(self):
        return Task(
            description="\n".join([
                "Take the final generated report (Markdown or summary).",
                "1. Use the `Send Report to Zapier` tool.",
                "2. Pass a suitable subject (like 'Inventory Report').",
                "3. Pass the report body text or summary.",
                "This will trigger Zapier → Gmail and send it to managers automatically."
            ]),
            agent=self.get_agent(),
            expected_output="Report successfully sent to Zapier → Gmail"
        )
