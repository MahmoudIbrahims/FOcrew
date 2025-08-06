from crewai import Task
from ..BaseAgent import BaseAgent
from Providers import ProviderLLM
from tools.FileReading import BatchFileReader,JsonBatchFileReader
from tools.BatchProcessing import BatchProcessor



class DataProcessing(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        batch_file_reader = BatchFileReader()
        Json_BatchFileReader = JsonBatchFileReader()
        Batch_Processor = BatchProcessor()

        super().__init__(
            name="Data Processing Specialist",
            role="Data Processing Specialist",
            goal="Process and analyze inventory data files efficiently regardless of size",
            backstory="\n".join([
                "You are a data processing expert who specializes in handling various file formats and sizes.",
                "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
            ]),
            llm=llm,
            allow_delegation=False,
            tools=[batch_file_reader, Json_BatchFileReader,Batch_Processor],
        )
        

    def get_task(self):
        return Task(
            description="".join([
                "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
                "1. Use the 'Batch Processor' tool to process ALL ",
                "2. Use only real data from the batch. ",
                "3. Save intermediate results per batch. ",
                "4. Combine into a final report. ",
                "5. save file in **results/inventory_management/data_analysis_report.md**"
            ]),
            agent=self.get_agent(),
            expected_output='results/inventory_management/data_analysis_report.md'
        )
