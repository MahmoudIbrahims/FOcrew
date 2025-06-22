from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool 


class InventoryOptimizationExpert(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        #file_tool = FileTool()
        super().__init__(
                    name="Inventory Optimization Expert",
                    role="Inventory Optimization Expert",
                    goal="Optimize inventory levels to minimize costs while avoiding stockouts",
                    backstory="\n".join([
                        "You are an inventory management expert who specializes in optimizing stock levels. ",
                        "You determine optimal reorder points, safety stock levels, and inventory policies to balance cost and service levels."
                        ]),
                    llm=llm,
                    allow_delegation=False
                        )
        
    
    def get_task(self):
        return Task(
                description="Optimize inventory levels and create management strategies",
                agent=self.get_agent(),
                expected_output="ABC classification, reorder points, and optimization recommendations"
            )
                    
            