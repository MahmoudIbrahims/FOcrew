import os
from crewai import Crew
from .AgentEnums import AgentName ,Languages

## marketingstratgeyplanner
from .AgentProvider import SWOTAnalyst
from .AgentProvider import MarketingStrategist
from .AgentProvider import  ContentPlanner
from .AgentProvider import TranslationEnglishArabic
## InventoryManagment
from .AgentProvider import DataProcessing
from .AgentProvider import DemandForecastingAnalyst
from .AgentProvider import InventoryOptimizationExpert
from .AgentProvider import InventoryAnalysisReportingSpecialist
from .AgentProvider import DataVisualizationExpert
from .AgentProvider import InventoryReportWriter



class AgentProviderFactory:
    def __init__(self,config : dict ):  
        self.config =config 
    
    def create(self, Crew_Name: str ,lanuage:str ,file_path:str):
        
        if Crew_Name == AgentName.MARKETING_STRATGEY_PLANNER.value:
            SWOT_Analyst = SWOTAnalyst()
            Marketing_Strategist = MarketingStrategist()
            Content_Planner = ContentPlanner()
            Translation_EnglishArabic =TranslationEnglishArabic()
            
    
            swot_agent = SWOT_Analyst.get_agent()
            swot_task = SWOT_Analyst.get_task()
            
            marketing_agent = Marketing_Strategist.get_agent()
            marketing_task = Marketing_Strategist.get_task()
            
            content_agent = Content_Planner.get_agent()
            content_task = Content_Planner.get_task()
            
            translation_agent =Translation_EnglishArabic.get_agent()
            translation_task =Translation_EnglishArabic.get_task()
            
            if lanuage== Languages.ARABIC.value:
                crew = Crew(
                    agents=[swot_agent,marketing_agent ,content_agent,translation_agent],
                    tasks=[swot_task ,marketing_task ,content_task,translation_task],
                    verbose=True
                                )
                
                result = crew.kickoff()
                output_dir = 'results/Agent_marketing'
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, 'marketing_analysis_arabic.md')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                
            elif lanuage== Languages.ENGLISH.value:
                crew = Crew(
                    agents=[swot_agent,marketing_agent ,content_agent],
                    tasks=[swot_task ,marketing_task ,content_task],
                    verbose=True
                                )
                
                result = crew.kickoff()
                
                output_dir = 'results/Agent_marketing'
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, 'marketing_analysis_english.md')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                    
        elif Crew_Name ==AgentName.INVENTORY_MANAGMENT.value:
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Inventory file not found:{file_path}")

            Data_Processing =DataProcessing()
        
            Data_Processing_Agent =Data_Processing.get_agent()
            Data_Processing_task =Data_Processing.get_task()
            Data_Processing_task.description ="\n".join([
                            f"Process the inventory data file: {file_path}",
                             "Process large inventory dataset in batches optimized for Gemini's context length. For each batch: ",
                                "1. Read the file Excel or CSV and split it into manageable batches. The `Optimized Batch File Reader` tool_1 save the results inside **results/Mini_Batches**",
                                "2. Read batch by batch to use `JsonBatchFileReader` tool_2",
                                "3. Use the `Batch Processor` tool_3 to process ALL and save resuts for this tool inside path **results/Mini_reports**",
                                "4. Use only real data from the batch. ",
                                "5. Save intermediate results per batch. ",
                                "6. Combine into a final report. ",
                                "## save the final report inside path **results/inventory_management/Analysis_Report.md**"
                            ])
            
            if lanuage== Languages.ARABIC.value:
                              
                crew = Crew(
                    agents=[Data_Processing_Agent],
                    
                    tasks=[Data_Processing_task],verbose=True)
                
                result = crew.kickoff()
                    
            elif lanuage== Languages.ENGLISH.value:
                crew = Crew(
                        agents=[Data_Processing_Agent],
                        
                        tasks=[Data_Processing_task],verbose=True)
                
                result = crew.kickoff()
                
               
            
                
                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
       
    
            
        
    
    
        
