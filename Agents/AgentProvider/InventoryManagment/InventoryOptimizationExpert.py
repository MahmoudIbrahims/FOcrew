from crewai import Task
from ..BaseAgent import BaseAgent
from models.ProviderLLM import ProviderLLM
from tools.FileReading import FileTool 


class InventoryOptimizationExpert(BaseAgent):
    def __init__(self):
        provider = ProviderLLM()
        llm = provider.get_llm()
        file_tool = FileTool()
        super().__init__(
                    name="Inventory Optimization Expert",
                    role="Inventory Optimization Expert",
                    goal="Optimize inventory levels to minimize costs while avoiding stockouts",
                    backstory="\n".join([
                        "You are an inventory management expert who specializes in optimizing stock levels. ",
                        "You determine optimal reorder points, safety stock levels, and inventory policies to balance cost and service levels."
                        ]),
                    llm=llm,
                    allow_delegation=False,
                    tools=[file_tool]
                        )
        
    
    def get_task(self):
        return Task(
            description="\n".join([
                "Optimize inventory levels and create inventory management strategies.",
                
                "Your responsibilities:",
                "1. Perform ABC analysis to classify inventory items",
                "2. Calculate optimal reorder points for each item",
                "3. Determine safety stock levels based on demand variability",
                "4. Calculate Economic Order Quantities (EOQ) where applicable",
                "5. Identify overstocked and understocked items",
                "6. Create inventory management policies for different item categories",
                
                "Consider factors like:",
                "- Demand forecasts from previous analysis",
                " - Lead times",
                "- Carrying costs",
                "- Stockout costs",
                "- Service level requirements",
    
                "Provide actionable optimization recommendations."
                
                             ]),
            agent=self.get_agent(),
            expected_output="\n".join([
                "Inventory optimization results including:",
                "- ABC classification for all items",
                "- Reorder points and safety stock levels",
                "- Current inventory status (overstocked/understocked/optimal)",
                " - Inventory management policies by category",
                "- Cost optimization opportunities",
                "- Priority actions list"
                    ]),
                )
            
            
            
            
            