from Agents.Prompts import Data_analysis_prompt
from Agents import DataAnalysisAgent
from fastapi import APIRouter ,status,Request,Depends
from helpers.config import get_settings, Settings
from Models.ProjectModel import ProjectModel
from Models.UserFileModel import UserFileModel
from fastapi.responses import JSONResponse
from .Schemes.data import DataAnaltsisRequest
from .Enums.BasicsEnums import Languages 
from Models.enums import ResponseSignal
from .Enums.DataAnalysisEnums import DataAnalysisEunms
from crewai import Crew


agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],
)


@agent_router.post('/DataAnalysis/{project_id}')
async def inventory_agent(request : Request ,project_id:int,DataAnaltsis_Request:DataAnaltsisRequest,
                          app_settings: Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client = request.app.db_client)

    model = await project_model.get_project_or_create_one(project_id = project_id )
    
    userfile_model =await UserFileModel.create_instance(db_client=request.app.db_client)
    
    latest_file = await userfile_model.get_latest_user_file_by_project(project_id =model.project_id)
        
    if not latest_file:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": ResponseSignal.RESPONSE_NOT_UPLOADED_FILE.value}
                 )  
        
    Agent_Analysis = DataAnalysisAgent()
    Agent_Analysis_Agent =Agent_Analysis.get_agent()
    Agent_Analysis_tesk =Agent_Analysis.get_task()
    Agent_Analysis_tesk.description =Data_analysis_prompt.safe_substitute(file_path=latest_file.file_path)
    
    if DataAnaltsis_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Agent_Analysis_Agent],
                    
                    tasks=[Agent_Analysis_tesk],
                    
                            verbose=True
                                )
                
        result = crew.kickoff()
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "Agent_name":DataAnalysisEunms.AGENT_NAME.value,
                    "created_at":str(latest_file.created_at)
                    
                }
        )
    
    

    
 





