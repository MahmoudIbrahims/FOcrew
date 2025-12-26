from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM


class UniversalTranslationAgent(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        super().__init__(
                name="Universal Translation Machine",
                role="Multilingual translation expert",
                goal="Translate content accurately between any two languages",
                backstory=(
                    "An expert AI linguist capable of translating text "
                    "between any pair of languages while preserving meaning, tone, "
                    "and formatting."
                ),
                llm=llm
            )
            
    def get_task(self):
        return Task(
            description="Translation from $source_language to $target_language and Preserve meaning, tone, and formatting.",
            agent=self.get_agent(),
            context_keys=["Markdown_report_path"],
            expected_output="Translation_report_path"
            )
