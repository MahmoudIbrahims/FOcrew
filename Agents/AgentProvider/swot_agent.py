from crewai import Agent,Task
from helpers.config import get_settings

def create_swot_agent(provider_namel):
    return Agent(
        role="SWOT Analyst",
        goal="Analyze company strengths, weaknesses, opportunities, and threats",
        backstory="Expert business analyst specializing in strategic analysis",
        llm=provider_namel.get_llm(),
        verbose=True
    )
    

def create_swot_task(swot_agent):
    settings = get_settings()
    return Task(
        description=f"Analyze {settings.COMPANY_NAME} in {settings.INDUSTRY_NAME} industry. Provide SWOT analysis with strengths, weaknesses, opportunities, and threats.",
        agent=swot_agent,
        expected_output="Detailed SWOT analysis report"
    )