from Agents.Prompts import data_reader_prompt,Convert_md_to_pdf_prompt
from Agents import (DataReaderAgent,DataCleanerAgent,
                    DataAnalyzerAgent,DataVisualizerAgent,ReportWriterAgent,ReportGeneratorAgent)

from fastapi import APIRouter ,status,Request,Depends,BackgroundTasks
from helpers.config import get_settings, Settings
from Models.ProjectModel import ProjectModel
from Models.UserFileModel import UserFileModel
from fastapi.responses import JSONResponse,FileResponse,StreamingResponse
from .Schemes.data import DataAnaltsisRequest
from .Enums.BasicsEnums import Languages
from Models.enums import ResponseSignal
from .Enums.DataAnalysisEnums import DataAnalysisEunms
from storage.S3.S3Provider import download_file_from_s3
from crewai import Crew
import os
import shutil
import time
from requests.exceptions import HTTPError
from pathlib import Path
import uuid



agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],

)


@agent_router.post('/DataAnalysis/{project_id}')

async def inventory_agent(request : Request ,project_id:int,DataAnaltsis_Request:DataAnaltsisRequest,backgroudtask:BackgroundTasks,

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

    base_dir = Path("data_analysis_jobs")

    unique_folder_name = f"project_{project_id}_{uuid.uuid4()}"

    job_dir_path = base_dir / unique_folder_name

    job_dir_path.mkdir(parents=True, exist_ok=True)

    full_local_file_path = job_dir_path / Path(latest_file.file_path).name

    final_pdf_path = job_dir_path / "Data_Analysis_Report.pdf"

    if not full_local_file_path.exists():

        try:

            download_file = download_file_from_s3(

                                boto3_client=request.app.storage_S3_client,
                                bucket_name=app_settings.AWS_BUCKET,
                                file_key=latest_file.file_path,
                                download_directory=job_dir_path.as_posix(),
                                force_download =True)

        except Exception as e:
            print(f"Error during S3 download: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": ResponseSignal.RESPONSE_NOT_DOWNLOAD_FILE.value})

        if not download_file:

            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": ResponseSignal.RESPONSE_NOT_DOWNLOAD_FILE.value}
                    )

    else:
        print(f"File already exists at: {full_local_file_path}")
        download_file = True

    Data_Reader = DataReaderAgent()
    Data_Reader_Agent =Data_Reader.get_agent()
    Data_Reader_task =Data_Reader.get_task()
    Data_Reader_task.description =data_reader_prompt.safe_substitute(file_path=full_local_file_path.as_posix())

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

    Report_Generator = ReportGeneratorAgent()
    Report_Generator_Agent =Report_Generator.get_agent()
    Report_Generator_task =Report_Generator.get_task()
    Report_Generator_task.description =Convert_md_to_pdf_prompt.safe_substitute(full_path=final_pdf_path.as_posix(),logo_company=app_settings.LOGO_COMPANY)

    if DataAnaltsis_Request.Language== Languages.ARABIC.value:
                   
        crew = Crew(

                    agents=[Data_Reader_Agent,Data_Cleaner_Agent,Data_Analyzer_Agent,

                            Data_Visualizer_Agent,Report_Writer_Agent,Report_Generator_Agent],

                    tasks=[Data_Reader_task,Data_Cleane_task,Data_Analyzer_task,Data_Visualizer_task,Report_Writer_task,Report_Generator_task],          
                              verbose=True
                             )

        MAX_RETRIES = 5
        BASE_WAIT_TIME = 5
        result = None
        for attempt in range(MAX_RETRIES):
            try:
                print(f"Attempting Crew Kickoff (Attempt {attempt + 1}/{MAX_RETRIES})...")
                result = crew.kickoff()
                break  
            
            except Exception as e:

                error_message = str(e)
                is_rate_limit_error = "RateLimitExceeded" in error_message or "429" in error_message

                if not is_rate_limit_error or attempt == MAX_RETRIES - 1:
                    print(f"Fatal error encountered: {error_message}")

                    return JSONResponse(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        content={"message": "Crew execution failed after retries."}

                    )

                wait_time = BASE_WAIT_TIME * (2 ** attempt)
                print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)

        if result is None:
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Crew execution failed unexpectedly."}

                         )
        
        response = None

        # if os.path.exists(final_pdf_path):
        #     backgroudtask.add_task(shutil.rmtree, job_dir_path)
        #     return FileResponse(
        #         path=final_pdf_path.as_posix(),
        #         filename="Data_Analysis_Report.pdf",
        #         media_type='application/pdf'

        #                    )

        if os.path.exists(final_pdf_path):
            #backgroudtask.add_task(shutil.rmtree, job_dir_path)

            def file_iterator(file_path):
                with open(file_path, "rb") as file_like:
                    yield from file_like


            file_name = "Data_Analysis_Report.pdf"

            headers = {
                    'Content-Disposition': f'inline; filename="{file_name}"' 
                     }
            
            return StreamingResponse(
                        file_iterator(final_pdf_path),
                        media_type='application/pdf',
                        headers=headers
                    )

        else:

            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Agent failed to generate the PDF report."}

                                )
        try:
            if job_dir_path.exists():
                print(f"Cleaning up job directory: {job_dir_path}")
                shutil.rmtree(job_dir_path)
                print("Cleanup successful.")

        except Exception as cleanup_e:
            print(f"Warning: Failed to cleanup directory {job_dir_path}. Error: {cleanup_e}")

        return response

