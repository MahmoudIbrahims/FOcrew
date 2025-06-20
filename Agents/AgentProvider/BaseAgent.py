from crewai import Agent
from langchain_core.language_models import BaseLanguageModel
from helpers.config import get_settings

class BaseAgent:
    def __init__(self, name: str, role: str, goal: str,backstory:str, llm: BaseLanguageModel):
        self.agent = Agent(
            name=name,
            role=role,
            goal=goal,
            backstory =backstory,
            llm=llm,
            verbose=True
        )

    def run(self, task_input: str) -> str:
        return self.agent.run(task_input)

    def get_agent(self) -> Agent:
        return self.agent
    
    def get_config(self) -> dict:
        return get_settings()
