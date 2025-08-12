from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from datetime import datetime


class InventoryReportWriter(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()

        super().__init__(
            name="Warehouse Inventory Report Writer",
            role="Professional Warehouse Inventory Analyst",
            goal="Transform processed inventory data into a professional warehouse analysis report in Markdown format.",
            backstory="\n".join([
                "You are an expert in warehouse inventory analysis and professional report writing.",
                "You specialize in turning complex inventory data into clear, actionable insights.",
                "Your reports help warehouse managers make strategic, data-driven decisions."
            ]),
            llm=llm,
            allow_delegation=False,
        )

    def get_task(self):
        return Task(
            description="\n".join([
                "You will receive processed and cleaned warehouse inventory data from a previous agent.",
                "Using this data, create a **professional Markdown report** for the warehouse manager.",
                "The report must include:",
                "1. Executive Summary – brief overview of the current inventory health.",
                "2. Key Warehouse Metrics – presented in a clean, well-formatted table.",
                "3. Top Financial Categories – ranked list in table format.",
                "4. Data Quality Review – highlight missing values in a table.",
                "5. Batch Processing Overview – table summarizing processing results.",
                "6. Recommendations – actionable suggestions to improve inventory management.",
                "",
                "Formatting requirements:",
                "- Use headings, bullet points, and tables.",
                "- Keep the tone professional and concise.",
                "",
                "Save the final report to: **results/inventory_management/finally_report.md**"
            ]),
            agent=self.get_agent(),
            expected_output="results/inventory_management/finally_report.md"
        )

