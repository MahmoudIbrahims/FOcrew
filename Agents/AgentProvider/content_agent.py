from crewai import Agent,Task

def create_content_agent(provider_namel):
    return Agent(
        role="Content Planner",
        goal="Plan and strategize content for marketing campaigns",
        backstory="Creative content strategist with expertise in multi-channel content planning",
        llm=provider_namel.get_llm(),
        verbose=True
    )
    

def Create_content_task(content_agent):
    return Task(
        description="Plan content strategy for the marketing campaign",
        agent=content_agent,
        expected_output="Content calendar and strategy"
    )
    