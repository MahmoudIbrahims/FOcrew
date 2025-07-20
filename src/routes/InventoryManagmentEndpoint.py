from fastapi import APIRouter ,status,Request
from Models.ProjectModel import ProjectModel
from Models.AgentResultModel import AgentResultModel
from Models.FileAgentRelationModel import FileAgentRelationModel
from Models.UserFileModel import UserFileModel
from Models.schema.DBSchemas import AgentResult  
import uuid
from .Schemes.data import ProcessRequest
from .AGRouterEnums import UsageType
from .AGRouterEnums import Languages 
from Models.enums import ResponseSignal
from crewai import Crew
from fastapi.responses import JSONResponse
from Agents import (DataAnalysisSpecialist,DemandForecastingAnalyst,InventoryOptimizationExpert,
                    InventoryAnalysisReportingSpecialist,DataVisualizationExpert ,TranslationEnglishArabic)

from Agents.Prompts import (finally_expected_output_prompt,Analysis_description_prompt,
                              Visualization_description_prompt,Visualization_expected_output_prompt,translation_description_prompt)

agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],
)

@agent_router.post('/inventory/{project_id}')
async def inventory_agent(request : Request ,project_id:int,Process_Request:ProcessRequest):
    
    userfile_model =await UserFileModel.create_instance(
         db_client = request.app.db_client
                     )

    project_model = await ProjectModel.create_instance( 
        db_client = request.app.db_client
        
                    )
    
    agent_model =await AgentResultModel.create_instance(
        db_client = request.app.db_client
        )
    
    agent_Relation_model =await FileAgentRelationModel.create_instance(
         db_client = request.app.db_client
                     )
    
    model = await project_model.get_project_or_create_one(
                project_id = project_id
                )
    
    latest_file = await userfile_model.get_latest_user_file_by_project(
                 project_id =model.project_id
                    )
        
    if not latest_file:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No uploaded file found for this project"}
        )
        
    Data_Processing =DataAnalysisSpecialist()
    Demand_ForecastingAnalyst =DemandForecastingAnalyst()
    Inventory_OptimizationExpert =InventoryOptimizationExpert()
    Inventory_AnalysisReportingSpecialist =InventoryAnalysisReportingSpecialist()
    Data_VisualizationExpert =DataVisualizationExpert()
        
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description =Analysis_description_prompt.safe_substitute( file_path =latest_file.full_data)

    Demand_ForecastingAnalyst_Agent =Demand_ForecastingAnalyst.get_agent()
    Demand_ForecastingAnalyst_task =Demand_ForecastingAnalyst.get_task()
            
    Inventory_OptimizationExpert_Agent =Inventory_OptimizationExpert.get_agent()
    Inventory_OptimizationExpert_task =Inventory_OptimizationExpert.get_task()
            
    Inventory_AnalysisReportingSpecialist_Agent =Inventory_AnalysisReportingSpecialist.get_agent()
    Inventory_AnalysisReportingSpecialist_task =Inventory_AnalysisReportingSpecialist.get_task()
    Inventory_AnalysisReportingSpecialist_task.expected_output= finally_expected_output_prompt.safe_substitute(
                    COMPANY_NAME=Process_Request.COMPANY_NAME,
                    INDUSTRY_NAME=Process_Request.INDUSTRY_NAME,
                    Language=Process_Request.Language
                    )
    Data_VisualizationExpert_agent = Data_VisualizationExpert.get_agent()
    Data_VisualizationExpert_task = Data_VisualizationExpert.get_task()
    Data_VisualizationExpert_task.description =Visualization_description_prompt.safe_substitute(file_path=latest_file.full_data)
    Data_VisualizationExpert_task.expected_output =Visualization_expected_output_prompt.safe_substitute(file_path=latest_file.full_data)
    
    translation_agent_provider = TranslationEnglishArabic()
    translation_agent = translation_agent_provider.get_agent()
    translation_task = translation_agent_provider.get_task()
    translation_task.description =translation_description_prompt.safe_substitute()
   
    if Process_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Data_Processing_Agent,
                            Demand_ForecastingAnalyst_Agent,
                            Inventory_OptimizationExpert_Agent,
                            Inventory_AnalysisReportingSpecialist_Agent,
                            Data_VisualizationExpert_agent,
                            translation_agent
                            ],
                    
                    tasks=[Data_Processing_task ,
                           Demand_ForecastingAnalyst_task,
                           Inventory_OptimizationExpert_task,
                           Inventory_AnalysisReportingSpecialist_task,
                           Data_VisualizationExpert_task,
                           translation_task],
                            verbose=True
                                )
                
        result = crew.kickoff()
        
        agent_result_Arabic = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=str(result), 
                    project_id=project_id,
                    agent_name="Inventory Managment Arabic",
                    status="completed"
                )
        
        agent  = await agent_model.create_agent_result(
                result = agent_result_Arabic
                )
        
        agent_Relation  = await agent_Relation_model.get_relation_or_create_one(
                     file_id=latest_file.file_id, 
                     agent_result_id = agent.result_id, 
                     usage_type =UsageType.INPUT.value
                     
                            )
        
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "results" : str(agent.result_data),
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
    
                    
    elif Process_Request.Language== Languages.ENGLISH.value:
        crew = Crew( 
                agents=[Data_Processing_Agent,
                        Demand_ForecastingAnalyst_Agent,
                        Inventory_OptimizationExpert_Agent,
                        Inventory_AnalysisReportingSpecialist_Agent,
                        Data_VisualizationExpert_agent
                                ],
                        
                tasks=[Data_Processing_task ,
                       Demand_ForecastingAnalyst_task,
                       Inventory_OptimizationExpert_task,
                       Inventory_AnalysisReportingSpecialist_task,
                       Data_VisualizationExpert_task],
                       verbose=True
                            )
                
        res = crew.kickoff()
        
        agent_result_English = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=str(res), 
                    project_id=project_id,
                    agent_name="Inventory Managment English",
                    status="completed"
                )
        
        agent  = await agent_model.create_agent_result(
                result = agent_result_English
                )
        
        
        agent_Relation  = await agent_Relation_model.get_relation_or_create_one(
                     file_id=latest_file.file_id, 
                     agent_result_id = agent.result_id, 
                     usage_type =UsageType.INPUT.value
                     
                            )
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "results" : str(agent.result_data),
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
                


        
        
        
  
    
    
   
    
    

            
    
  
    
  
    
   
    
    
                                
    
    
    
   
    