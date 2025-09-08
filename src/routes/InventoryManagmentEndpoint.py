from fastapi import APIRouter ,status,Request,Depends
from Models.ProjectModel import ProjectModel
from Models.AgentResultModel import AgentResultModel
from Models.FileAgentRelationModel import FileAgentRelationModel
from Agents.Prompts import (Data_processing_prompt,description_prompt,
                                                 Visualization_Prompt)
from helpers.config import get_settings, Settings
from Models.UserFileModel import UserFileModel
from Agents import DataProcessing,DataVisualizationExpert,ReportGeneratorAgent
from Models.schema.DBSchemas import AgentResult  
from .Schemes.data import ProcessRequest
from .Enums.BasicsEnums import UsageType
from .Enums.BasicsEnums import Languages 
from .Enums.InventorymanagmentEnums import InventorManagmentEunms ,PathResults
from Models.enums import ResponseSignal
from crewai import Crew
from fastapi.responses import JSONResponse
import uuid
import os
from datetime import datetime
from pandas import Timestamp
import PyPDF2


agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],
)


def convert_to_json_serializable(obj):
    if isinstance(obj, (datetime, Timestamp)):
        return obj.isoformat()
    elif isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    return str(obj)


def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


def read_pdf(file_path:str):
    reader = PyPDF2.PdfReader(file_path)
    text_content = ""

    for page in reader.pages:
        text_content += page.extract_text() or ""

    return {
        "filename": file_path,
        "content": text_content
    }
    

@agent_router.post('/inventory/{project_id}')
async def inventory_agent(request : Request ,project_id:int,Process_Request:ProcessRequest,
                          app_settings: Settings = Depends(get_settings)):
    
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
            content={
                "message": ResponseSignal.RESPONSE_NOT_UPLOADED_FILE.value}
                 )
    
    full_data = convert_to_json_serializable(latest_file.full_data)
        
    Data_Processing =DataProcessing()
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description =Data_processing_prompt.safe_substitute(full_data=full_data)
    
    Data_Visualization =DataVisualizationExpert()
    Data_Visualization_Agent =Data_Visualization.get_agent()
    Data_Visualization_task =Data_Visualization.get_task()
    Data_Visualization_task.description =Visualization_Prompt.safe_substitute(full_data=full_data)
    
    
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
        
        analysis_report_content =read_file_content(PathResults.ANALYSIS_REPORT_PATH.value) if os.path.exists(PathResults.ANALYSIS_REPORT_PATH.value) else "Analysis report not found"
        profiling_report_content =read_file_content(PathResults.PROFILLING_REPORT_PATH.value) if os.path.exists(PathResults.PROFILLING_REPORT_PATH.value) else "Profiling report not found"
        report_pdf =read_pdf(PathResults.REPORT_PDF.value) if os.path.exists(PathResults.REPORT_PDF.value) else "report pdf not found"
        
        combined_result = {
            # "crew_result": str(result),
            # "analysis_report": analysis_report_content,
            # "profiling_report": profiling_report_content,
            "report_pdf":report_pdf
        }
        
        agent_result = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=combined_result, 
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
                    "results" : combined_result,
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
    
    