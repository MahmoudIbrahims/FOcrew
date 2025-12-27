#=================DataAnalysis=====================
from .AgentProvider import DataReaderAgent
from .AgentProvider import DataCleanerAgent
from .AgentProvider import DataAnalyzerAgent
from .AgentProvider import DataVisualizerAgent
from .AgentProvider import ReportWriterAgent
from .AgentProvider import ReportGeneratorAgent
from .AgentProvider import ReportSenderAgent
#===================Prompts===========================
from .Prompts.DataReaderPrompt import data_reader_prompt
from .Prompts.DataCleanerPrompt import cleaning_prompt
from .Prompts.DataAnalyzerPrompt import analysis_prompt
from .Prompts.DataVisualizerPrompt import visualizations_prompt
from .Prompts.ReportWriterPrompt import report_writer_prompt
from .Prompts.MarkdownToPDFReportPrompt import Convert_md_to_pdf_prompt
from .Prompts.SendEmailprompt import SendEmail_prompt
#=======================================
import os
from crewai import Crew
from .AgentEnums import AgentName ,Languages
from tools.run_command_tool import RunCommandTool
from typing import Optional
from pathlib import Path
import uuid


class AgentProviderFactory:
    def __init__(self,config : dict ):  
        self.config =config 
    
    def create(self, Crew_Name: str ,lanuage:str,
                                        Managers:str,file_path: Optional[str] = None):
        
        if Crew_Name == AgentName.DATA_ANALYSIS_AGENT.value:

            if not file_path or not Path(file_path).exists():
                print(f"file not found: {file_path}, skipping...")
                file_path = None


            SRC_DIR = Path(__file__).resolve().parent
            OUTPUT_DIR = SRC_DIR / "data_analysis_results"

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            working_dir =OUTPUT_DIR / str(uuid.uuid4())

            final_md_path = OUTPUT_DIR / "final_report.md"

            final_pdf_path = OUTPUT_DIR / "final_report.pdf"

            cmd_tool = RunCommandTool(
                    working_dir=working_dir.as_posix()
                    )

            Data_Reader = DataReaderAgent(cmd_tool)
            Data_Reader_Agent =Data_Reader.get_agent()
            Data_Reader_task =Data_Reader.get_task()
            Data_Reader_task.description =data_reader_prompt.safe_substitute(working_dir=working_dir.as_posix(),file_path=file_path)

            Data_Cleaner = DataCleanerAgent(cmd_tool)
            Data_Cleaner_Agent =Data_Cleaner.get_agent()
            Data_Cleaner_task =Data_Cleaner.get_task()
            Data_Cleaner_task.description=cleaning_prompt.safe_substitute(working_dir=working_dir.as_posix())

            Data_Analyzer = DataAnalyzerAgent(cmd_tool)
            Data_Analyzer_Agent =Data_Analyzer.get_agent()
            Data_Analyzer_task =Data_Analyzer.get_task() 
            Data_Analyzer_task.description=analysis_prompt.safe_substitute(working_dir =working_dir.as_posix())
            
            Data_Visualizer = DataVisualizerAgent(cmd_tool)
            Data_Visualizer_Agent =Data_Visualizer.get_agent()
            Data_Visualizer_task =Data_Visualizer.get_task()
            Data_Visualizer_task.description=visualizations_prompt.safe_substitute(working_dir=working_dir.as_posix())

            Report_Writer = ReportWriterAgent()
            Report_Writer_Agent =Report_Writer.get_agent()
            Report_Writer_task =Report_Writer.get_task()
            Report_Writer_task.description =report_writer_prompt.safe_substitute(report_md_path=final_md_path.as_posix(),working_dir=working_dir.as_posix(),target_language=lanuage)

            Report_Generator = ReportGeneratorAgent(cmd_tool)
            Report_Generator_Agent =Report_Generator.get_agent()
            Report_Generator_task =Report_Generator.get_task()
            Report_Generator_task.description =Convert_md_to_pdf_prompt.safe_substitute(working_dir=working_dir.as_posix(),file_path=final_md_path.as_posix(),
                                                                                        output_report=final_pdf_path.as_posix())
            ReportSender_Agent=ReportSenderAgent()
            Report_Sender_Agent =ReportSender_Agent.get_agent()
            Report_Sender_tesk =ReportSender_Agent.get_task()
            Report_Sender_tesk.description =SendEmail_prompt.safe_substitute(working_dir=working_dir.as_posix(),file_path =final_pdf_path.as_posix(),managers=Managers)

            agents = [
                    Data_Reader_Agent,
                    Data_Cleaner_Agent,
                    Data_Analyzer_Agent,
                    Data_Visualizer_Agent,
                    Report_Writer_Agent,
                    Report_Generator_Agent,
                    Report_Sender_Agent
                ]

            tasks = [
                Data_Reader_task,
                Data_Cleaner_task,
                Data_Analyzer_task,
                Data_Visualizer_task,
                Report_Writer_task,
                Report_Generator_task,
                Report_Sender_tesk

            ]
         

            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True
            )
            result = crew.kickoff()

        else:
            print("Skip the Provider Factory.....")




            
            
            
            
            
            
            
            
            
            
            
            
        
       
    
            
        
    
    
        
