from crewai import Agent,Task

def create_translation_agent(provider_namel):
    return Agent(
        role="translation english to arabic",
        goal="Translation English to Egyption Arabic",
        backstory="Expert translation English to Arabic",
        llm=provider_namel.get_llm(),
        verbose=True
    )
    

def create_translation_task(translation_agent):
    return Task(
        description="Translation English to Egyption Arabic ",
        agent=translation_agent,
        expected_output="text Egyption arabic"
        )
