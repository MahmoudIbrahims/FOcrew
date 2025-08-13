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
                            f"Process the inventory data file:$file_path",
                             "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
                                "1. Read the file Excel or CSV and split it into manageable batches. The `Optimized Batch File Reader` tool_1 save the results inside **results/Mini_Batches**",
                                "2. Read batch by batch to use `JsonBatchFileReader` tool_2",
                                "3. Use the `Batch Processor` tool_3 to process ALL and save resuts for this tool inside path **results/Mini_reports**",
                                "4. Use only real data from the batch. ",
                                "5. Save intermediate results per batch. ",
                                "6. Combine into a final report. ",
                                "## save the final report inside path **results/inventory_management/Analysis_Report.md**"
                            ]), 
            agent=self.get_agent(),
            expected_output="final report markdown"
                            
        )
