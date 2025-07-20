from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from datetime import datetime
from ...Prompts import finally_description_prompt, finally_expected_output_prompt


class InventoryAnalysisReportingSpecialist(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        
        super().__init__(
            name="Inventory Analysis & Reporting Specialist",
            role="Senior Inventory Analysis & Strategic Reporting Specialist",
            goal="Create comprehensive inventory reports with clear sections for each analysis type and actionable insights",
            backstory="Senior inventory analyst with 10+ years experience in supply chain optimization. Expert in transforming complex data into executive-ready reports with strategic recommendations.",
            llm=llm,
            allow_delegation=False,
        )
    
    def get_task(self):
        return Task(
             description= finally_description_prompt.template,
            agent=self.get_agent(),
            expected_output= finally_expected_output_prompt.safe_substitute(
                COMPANY_NAME = self.get_config().COMPANY_NAME,
                INDUSTRY_NAME =self.get_config().INDUSTRY_NAME,
                Language= self.get_config().LANGUAGE),
            
            output_file="results/inventory_management/comprehensive_inventory_analysis_report.md"
        )
        
        