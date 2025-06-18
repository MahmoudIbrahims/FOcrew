from .AgentEnums import AgentNAME     
from .AgentProvider.content_agent import create_content_agent,Create_content_task
from .AgentProvider.marketing_agent import create_marketing_agent ,create_marketing_task
from .AgentProvider.swot_agent import create_swot_agent,create_swot_task
from .AgentProvider.translation_agent import create_translation_agent ,create_translation_task
from  models.ProviderLLM import ProviderLLM
from crewai import Crew


class AgentProviderFactory:
    
    def __init__(self,config : dict ):
        
        self.config =config 
    
    def create(self, Crew_Name: str):
        
        if Crew_Name == AgentNAME.MARKETING_STRATGEY_PLANNER.value:
            
            ProviderLLM_instance = ProviderLLM()
            
            swot_agent = create_swot_agent(ProviderLLM_instance)
            swot_task = create_swot_task(swot_agent)
            
            marketing_agent = create_marketing_agent(ProviderLLM_instance)
            marketing_task = create_marketing_task(marketing_agent)
            
            content_agent = create_content_agent(ProviderLLM_instance)
            content_task = Create_content_task(content_agent)
            
            translation_agent =create_translation_agent(ProviderLLM_instance)
            translation_task =create_translation_task(translation_agent)
            
            crew = Crew(
            agents=[swot_agent,marketing_agent ,content_agent,translation_agent],
            tasks=[swot_task ,marketing_task ,content_task,translation_task],
            verbose=True
                        )
        
            result = crew.kickoff()
            
        with open('results/Agent_marketing/marketing_analysis_arabic.md', 'w') as f:
                f.write(str(result))
        
        return {
            "status":"Done"
        }
            
       
    
            
        
    
    
        
