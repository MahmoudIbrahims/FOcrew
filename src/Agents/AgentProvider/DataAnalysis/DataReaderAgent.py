from crewai import Task
from tools.file_tool import FileReaderTool
from Providers import ProviderLLM
from ..BaseAgent import BaseAgent

class DataReaderAgent(BaseAgent):
    def __init__(self):
        llm = ProviderLLM().get_llm()
        reader_tool = FileReaderTool()
        super().__init__(
            name="DataReaderAgent",
            role="Data Reader",
            goal="Load and summarize the dataset structure.",
            backstory="Specialist in reading and understanding dataset schemas.",
            llm=llm,
            tools=[reader_tool],
        )

    def get_task(self):
        return Task(
            description=(
                "Read and summarize the dataset file provided at $file_path.\n\n"
                "Steps:\n"
                "1. Detect the file type (CSV, Excel, or JSON).\n"
                "2. Load the dataset into a pandas DataFrame.\n"
                "3. Display the first few rows and dataset structure (columns, types, shape).\n"
                "4. Return a Markdown-formatted summary including shape, columns, dtypes, and sample data."
            ),
            expected_output="A summary of the dataset structure, column details, and head preview.",
            agent=self.get_agent(),
            output_key="dataset_summary"
        )
