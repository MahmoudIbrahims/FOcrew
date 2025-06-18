from crewai import Agent,Task

def create_marketing_agent(provider_namel):
    return Agent(
        role="Marketing Strategist",
        goal="Create comprehensive marketing plans and strategies",
        backstory="Experienced marketing professional with expertise in campaign planning",
        llm=provider_namel.get_llm(),
        verbose=True
    )
    
def create_marketing_task(marketing_agent):
    return Task(
        description="Create marketing plan based on the SWOT analysis results",
        agent=marketing_agent,
        expected_output="Comprehensive marketing strategy"
    )