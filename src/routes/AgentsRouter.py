from fastapi import FastAPI, APIRouter ,Depends,UploadFile,status,Request
from Agents import (DataProcessing,DemandForecastingAnalyst,InventoryOptimizationExpert,
                    InventoryAnalysisReportingSpecialist,TranslationEnglishArabic)
from helpers.config import get_settings ,Settings
from AGRouterEnums import Languages ,ResponseSignal
from crewai import Crew
from fastapi.responses import JSONResponse
from fastapi import File, Form

agent_router = APIRouter(
    prefix ="/api/v1",
    tags =["api_v1"],
)


@agent_router.post('/agent/inventory')
async def inventory_agent(file : UploadFile=File(...),Language: str = Form(...),
                                                COMPANY_NAME: str = Form(...),
                                                INDUSTRY_NAME: str = Form(...)):
    
    Data_Processing =DataProcessing()
    Demand_ForecastingAnalyst =DemandForecastingAnalyst()
    Inventory_OptimizationExpert =InventoryOptimizationExpert()
    Inventory_AnalysisReportingSpecialist =InventoryAnalysisReportingSpecialist()
        
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description ="\n".join([
                            f"Process the inventory data file: {file}",
                            
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
            
    if Language== Languages.ARABIC.value:
                              
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
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "resultS" : str(result)
                    
                }
        )
    
                    
    elif Language== Languages.ENGLISH.value:
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
                
        res = crew.kickoff()
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "resultS" : str(res)
                    
                }
        )
                

