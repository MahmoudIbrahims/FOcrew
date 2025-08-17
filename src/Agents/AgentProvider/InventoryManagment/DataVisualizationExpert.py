from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.dashboard_tool import MarkdownTableReader  

class DataVisualizationExpert(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        markdown_reader = MarkdownTableReader()

        super().__init__(
            name="Markdown Analysis Specialist",
            role="Markdown Data Analyst",
            goal="Read and analyze markdown tables and generate profiling reports",
            backstory="\n".join([
                "You are an expert in processing and analyzing data embedded in markdown files.",
                "You can extract tables from markdown, clean the data, and produce detailed profiling reports."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[markdown_reader],
        )
        

    def get_task(self):
        return Task(
            description="\n".join([
                f"Process the inventory data file:$file_path",  
                "1. Use the `MarkdownTableReader` tool to read and clean all data from the file. ",
                "2. Generate a profiling HTML report from dataset ",
                "3. Save the profiling report in the same directory as the markdown file with `_profile.html` suffix. ",
                "## finally save the report HTML in **'results/Dashboard'**"
            ]),
            agent=self.get_agent(),
            expected_output="Cleaned tables list and profiling HTML report"
        )

