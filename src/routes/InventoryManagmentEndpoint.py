from Agents.Prompts import Data_processing_prompt,description_prompt,Visualization_Prompt
from Agents import DataProcessing,DataVisualizationExpert,ReportGeneratorAgent
from .Enums.InventorymanagmentEnums import InventorManagmentEunms
from fastapi import APIRouter ,status,Request,Depends
from helpers.config import get_settings, Settings
from Models.ProjectModel import ProjectModel
from Models.UserFileModel import UserFileModel
from fastapi.responses import JSONResponse
from .Schemes.data import ProcessRequest
from .Enums.BasicsEnums import UsageType
from .Enums.BasicsEnums import Languages 
from Models.enums import ResponseSignal
from crewai import Crew
import pandas as pd

agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],
)


@agent_router.post('/inventory/{project_id}')
async def inventory_agent(request : Request ,project_id:int,Process_Request:ProcessRequest,
                          app_settings: Settings = Depends(get_settings)):
    
    userfile_model =await UserFileModel.create_instance(
         db_client = request.app.db_client
                     )

    project_model = await ProjectModel.create_instance( 
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
            content={
                "message": ResponseSignal.RESPONSE_NOT_UPLOADED_FILE.value}
                 )    
    
    Data_Processing =DataProcessing()
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description =Data_processing_prompt.safe_substitute(file_path=latest_file.file_path)
    
    Data_Visualization =DataVisualizationExpert()
    Data_Visualization_Agent =Data_Visualization.get_agent()
    Data_Visualization_task =Data_Visualization.get_task()
    Data_Visualization_task.description =Visualization_Prompt.safe_substitute(file_path=latest_file.file_path)
    
    
    ReportGenerator =ReportGeneratorAgent()
    ReportGenerator_Agent =ReportGenerator.get_agent()
    ReportGenerator_task =ReportGenerator.get_task()
    ReportGenerator_task.description =description_prompt.safe_substitute(logo_company=app_settings.LOGO_COMPANY)

    if Process_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Data_Processing_Agent,
                            Data_Visualization_Agent,ReportGenerator_Agent],
                    
                    tasks=[Data_Processing_task ,
                           Data_Visualization_task,ReportGenerator_task],
                            verbose=True
                                )
                
        result = crew.kickoff()
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "Agent_name":InventorManagmentEunms.AGENT_NAME.value,
                    "created_at":str(latest_file.created_at)
                    
                }
        )
    
    