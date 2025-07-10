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
            Demand_ForecastingAnalyst =DemandForecastingAnalyst()
            Inventory_OptimizationExpert =InventoryOptimizationExpert()
            Inventory_AnalysisReportingSpecialist =InventoryAnalysisReportingSpecialist()
        
            Data_Processing_Agent =Data_Processing.get_agent()
            Data_Processing_task =Data_Processing.get_task()
            Data_Processing_task.description ="\n".join([
                            f"Process the inventory data file: {file_path}",
                            
                            "Your responsibilities:",
                            "1. Read and analyze the file structure",
                            "2. Validate data quality and identify any issues",
                            "3. Extract key information about inventory items",
                            "4. Prepare clean data summary for further analysis",
                            "5. Identify data patterns and basic statistics",
                            
                            "Provide a comprehensive data summary."
                            ])
            
            Demand_ForecastingAnalyst_Agent =Demand_ForecastingAnalyst.get_agent()
            Demand_ForecastingAnalyst_task =Demand_ForecastingAnalyst.get_task()
            
            Inventory_OptimizationExpert_Agent =Inventory_OptimizationExpert.get_agent()
            Inventory_OptimizationExpert_task =Inventory_OptimizationExpert.get_task()
            
            Inventory_AnalysisReportingSpecialist_Agent =Inventory_AnalysisReportingSpecialist.get_agent()
            Inventory_AnalysisReportingSpecialist_task =Inventory_AnalysisReportingSpecialist.get_task()
            
            translation_agent_provider = TranslationEnglishArabic()
            translation_agent = translation_agent_provider.get_agent()
            translation_task = translation_agent_provider.get_task()
            translation_task.description ="\n".join([
                        "Translate the comprehensive inventory analysis report from English to Arabic.",
                        "Ensure technical terms are accurately translated and the report maintains its professional structure and actionable insights."
                                        ])
            
            if lanuage== Languages.ARABIC.value:
                              
                crew = Crew(
                    agents=[Data_Processing_Agent,
                            Demand_ForecastingAnalyst_Agent,
                            Inventory_OptimizationExpert_Agent,
                            Inventory_AnalysisReportingSpecialist_Agent,
                            translation_agent
                            ],
                    
                    tasks=[Data_Processing_task ,
                           Demand_ForecastingAnalyst_task,
                           Inventory_OptimizationExpert_task,
                           Inventory_AnalysisReportingSpecialist_task,
                           translation_task],
                            verbose=True
                                )
                
                result = crew.kickoff()
                    
            elif lanuage== Languages.ENGLISH.value:
                crew = Crew(
                        agents=[Data_Processing_Agent,
                                Demand_ForecastingAnalyst_Agent,
                                Inventory_OptimizationExpert_Agent,
                                Inventory_AnalysisReportingSpecialist_Agent
                                ],
                        
                        tasks=[Data_Processing_task ,
                            Demand_ForecastingAnalyst_task,
                            Inventory_OptimizationExpert_task,
                            Inventory_AnalysisReportingSpecialist_task],
                                verbose=True
                                    )
                
                result = crew.kickoff()
                
               
            
                
                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
       
    
            
        
    
    
        
