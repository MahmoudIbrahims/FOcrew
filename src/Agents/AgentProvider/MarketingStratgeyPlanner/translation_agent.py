from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM


class TranslationEnglishArabic(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        super().__init__(
                    name="translation English to Arabic",
                    role="translation english to Egyption arabic",
                    goal="Translation English to Egyption Arabic",
                    backstory="Expert translation English to Arabic",
                    llm=llm
                   
                    )
        
    def get_task(self):
        return Task(
            description="Translation English to Egyption Arabic ",
            agent=self.get_agent(),
            expected_output="text Egyption arabic"
            )
