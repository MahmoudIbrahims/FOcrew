from fastapi import APIRouter ,status,Request
from Models.ProjectModel import ProjectModel
from Models.AgentResultModel import AgentResultModel
from Models.FileAgentRelationModel import FileAgentRelationModel
from Agents.Prompts import (Data_processing_prompt,
                                                 Visualization_Prompt)
from Models.UserFileModel import UserFileModel
from Agents import DataProcessing,DataVisualizationExpert
from Models.schema.DBSchemas import AgentResult  
from .Schemes.data import ProcessRequest
from .Enums.BasicsEnums import UsageType
from .Enums.BasicsEnums import Languages 
from .Enums.InventorymanagmentEnums import InventorManagmentEunms 
from Models.enums import ResponseSignal
from crewai import Crew
from fastapi.responses import JSONResponse
import uuid


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
        
    Data_Processing =DataProcessing()
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description =Data_processing_prompt.safe_substitute(full_data=latest_file.full_data)
    
    Data_Visualization =DataVisualizationExpert()
    Data_Visualization_Agent =Data_Visualization.get_agent()
    Data_Visualization_task =Data_Visualization.get_task()
    Data_Visualization_task.description =Visualization_Prompt.safe_substitute(full_data=latest_file.full_data)

    if Process_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Data_Processing_Agent,
                            Data_Visualization_Agent],
                    
                    tasks=[Data_Processing_task ,
                           Data_Visualization_task],
                            verbose=True
                                )
                
        result = crew.kickoff()
        
        agent_result = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=str(result), 
                    project_id=project_id,
                    agent_name=InventorManagmentEunms.AGENT_NAME.value,
                    status=InventorManagmentEunms.STATUS.value
                )
        
        agent  = await agent_model.create_agent_result(
                result = agent_result
                )
        
        agent_Relation  = await agent_Relation_model.get_relation_or_create_one(
                     file_id=latest_file.file_id, 
                     agent_result_id = agent.result_id, 
                     usage_type =UsageType.INPUT.value
                     
                            )
        
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "agent name":str(agent.agent_name),
                    "results" : str(agent.result_data),
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
    
    