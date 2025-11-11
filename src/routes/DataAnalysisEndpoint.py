from Agents.Prompts import data_reader_prompt
from Agents import (DataReaderAgent,DataCleanerAgent,
                    DataAnalyzerAgent,DataVisualizerAgent,ReportWriterAgent)
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
        
    Data_Reader = DataReaderAgent()
    Data_Reader_Agent =Data_Reader.get_agent()
    Data_Reader_task =Data_Reader.get_task()
    Data_Reader_task.description =data_reader_prompt.safe_substitute(file_path=latest_file.file_path)

    Data_Cleaner = DataCleanerAgent()
    Data_Cleaner_Agent =Data_Cleaner.get_agent()
    Data_Cleane_task =Data_Cleaner.get_task()

    Data_Analyzer = DataAnalyzerAgent()
    Data_Analyzer_Agent =Data_Analyzer.get_agent()
    Data_Analyzer_task =Data_Analyzer.get_task()

    Data_Visualizer = DataVisualizerAgent()
    Data_Visualizer_Agent =Data_Visualizer.get_agent()
    Data_Visualizer_task =Data_Visualizer.get_task()

    Report_Writer = ReportWriterAgent()
    Report_Writer_Agent =Report_Writer.get_agent()
    Report_Writer_task =Report_Writer.get_task()
    
    if DataAnaltsis_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Data_Reader_Agent,Data_Cleaner_Agent,Data_Analyzer_Agent,
                            Data_Visualizer_Agent,Report_Writer_Agent],
                    
                    tasks=[Data_Reader_task,Data_Cleane_task,Data_Analyzer_task,Data_Visualizer_task,Report_Writer_task],
                    
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
    
    

    
 





