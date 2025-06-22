from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool,DirectoryTool 


class DataProcessing(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        file_tool = FileTool()
        directory_tool =DirectoryTool()
        super().__init__(
                    name="Data Processing Specialist",
                    role="Data Processing Specialist",
                    goal="Process and analyze inventory data files efficiently regardless of size",
                    backstory="\n".join([
                        "You are a data processing expert who specializes in handling various file formats and sizes."
                        "You can efficiently read, clean, and prepare inventory data for analysis, ensuring data quality and consistency."
                        ]),
                    llm=llm,
                    allow_delegation=False,
                    tools=[file_tool,directory_tool] 
            
                     )
        
    def get_task(self):
        return Task(
            description="\n".join([
                "Process the inventory data and prepare it for analysis",
                "Your responsibilities:",
                "1. Read and analyze the file structure",
                "2. Validate data quality and identify any issues",
                "3. Extract key information about inventory items",
                "4. Prepare clean data summary for further analysis",
                "5. Identify data patterns and basic statistics",
                
                "Ensure the data is properly formatted with:",
                "- Item IDs/Names",
                "- Current stock levels",
                "- Sales history",
                "- Unit costs",
                "- Any other relevant inventory metrics",
    
                "Provide a comprehensive data summary."
                
                
                ]),
            agent=self.get_agent(),
            expected_output="\n".join([
                "A detailed data summary including:",
                "- Total number of inventory items",
                "- Data quality assessment",
                "- Basic statistics (min, max, average stock levels)",
                "- Sample of processed data",
                "- Any data issues identified ."
                    ])
                )
        