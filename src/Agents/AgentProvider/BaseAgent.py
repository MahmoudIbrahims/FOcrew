from crewai import Agent
from langchain_core.language_models import BaseLanguageModel
from helpers.config import get_settings

class BaseAgent:
    def __init__(self, name: str, role: str, goal: str,backstory:str, llm: BaseLanguageModel,
                                                    allow_delegation: bool = False,tools: list = None,
                                                    reasoning: bool =False,  # Enable reasoning
                                                    max_reasoning_attempts:int =3):
        self.agent = Agent(
            name=name,
            role=role,
            goal=goal,
            backstory =backstory,
            llm=llm,
            verbose=True,
            allow_delegation=allow_delegation,
            tools= tools if tools else [],
            reasoning=reasoning,
            max_reasoning_attempts=max_reasoning_attempts
            
        )

    def run(self, task_input: str) -> str:
        return self.agent.run(task_input)

    def get_agent(self) -> Agent:
        return self.agent
    
    def get_config(self) -> dict:
        return get_settings()
