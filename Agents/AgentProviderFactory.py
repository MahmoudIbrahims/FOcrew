import os
from crewai import Crew
from .AgentEnums import AgentName  
from .AgentProvider import SWOTAnalyst
from .AgentProvider import MarketingStrategist
from .AgentProvider import  ContentPlanner
from .AgentProvider import TranslationEnglishArabic


class AgentProviderFactory:
    
    def __init__(self,config : dict ):
        
        self.config =config 
    
    def create(self, Crew_Name: str):
        
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
            
        
       
    
            
        
    
    
        
