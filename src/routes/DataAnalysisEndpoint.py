from Agents.Prompts import (data_reader_prompt,cleaning_prompt,
                                analysis_prompt,visualizations_prompt,report_writer_prompt,
                                    Translation_prompt,Convert_md_to_pdf_prompt,SendEmail_prompt)

from Agents import (DataReaderAgent,DataCleanerAgent,DataAnalyzerAgent,
                            DataVisualizerAgent,ReportWriterAgent,ReportGeneratorAgent,
                                        ReportSenderAgent,UniversalTranslationAgent)

from fastapi import APIRouter ,status,Request,Depends,BackgroundTasks
from fastapi.responses import JSONResponse,FileResponse
from storage.S3.S3Provider import download_file_from_s3
from tools.run_command_tool import RunCommandTool
from helpers.config import get_settings, Settings
from Models.ProjectModel import ProjectModel
from Models.UserFileModel import UserFileModel
from .Schemes.data import ProcessRequest
from .Enums.BasicsEnums import Languages
from Models.enums import ResponseSignal
from requests.exceptions import HTTPError
from pathlib import Path
from crewai import Crew
import os
import shutil
import time
import uuid


agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],

)

@agent_router.post('/DataAnalysis/{project_id}')
async def inventory_agent(
        request :Request,
        project_id:str,
        DataAnalysis_Request:ProcessRequest,
        backgroudtask:BackgroundTasks,
        app_settings: Settings = Depends(get_settings)):
    
    """
    Endpoint to perform full data analysis for a specific project.

    Steps:
    1. Validate project ID and fetch project details from the database.
    2. Retrieve the latest uploaded file for the project (from local storage or S3).
    3. Create a temporary working directory for analysis files.
    4. Run a series of Crew AI agents to:
       - Read and summarize the dataset (DataReaderAgent)
       - Clean the data (DataCleanerAgent)
       - Analyze data and extract insights (DataAnalyzerAgent)
       - Create visualizations (DataVisualizerAgent)
       - Write a Markdown report (ReportWriterAgent)
       - Optionally translate the report (UniversalTranslationAgent)
       - Convert Markdown to PDF (ReportGeneratorAgent)
       - Send the final PDF via email (ReportSenderAgent)
    5. Handle rate limit retries for Crew execution.
    6. Return the generated PDF report if successful.

    Path Parameters:
        project_id (str): The ID of the project to analyze.

    Request Body:
        DataAnalysis_Request (ProcessRequest):
            - Language: Report language ("en" or "ar" or fr or gr)
            - COMPANY_NAME: Company name
            - INDUSTRY_NAME: Industry type
            - MANAGER_EMAIL: Email to send the report

    Responses:
        200: Returns PDF report.
        400: Project ID missing.
        404: File not found or failed to download from S3.
        500: Agent execution failed or report generation failed.
        503: Crew execution failed after retries (rate limit or temporary issue).
    """
    
    if not project_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Project ID is required in URL."}
        )

    project_model = await ProjectModel.create_instance(
                                        db_client = request.app.db_client)

    model = await project_model.get_project_by_id(project_id)

    Update_record = await project_model.update_project(
                            project_id=project_id,
                            company_name=DataAnalysis_Request.COMPANY_NAME,
                            industry_name =DataAnalysis_Request.INDUSTRY_NAME,
                            report_language =DataAnalysis_Request.Language
                                )

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

    final_md_path = job_dir_path / "Data_Analysis_Report.md"

    final_pdf_path = job_dir_path / "Data_Analysis_Report.pdf"

    cmd_tool = RunCommandTool(
        working_dir=job_dir_path.as_posix()
                    )

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

    
    if not full_local_file_path.exists():
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "The file for this project does not exist."}
        )

    Data_Reader = DataReaderAgent(cmd_tool)
    Data_Reader_Agent =Data_Reader.get_agent()
    Data_Reader_task =Data_Reader.get_task()
    Data_Reader_task.description =data_reader_prompt.safe_substitute(file_path=full_local_file_path.as_posix(),
                                                                     working_dir=job_dir_path.as_posix())

    Data_Cleaner = DataCleanerAgent(cmd_tool)
    Data_Cleaner_Agent =Data_Cleaner.get_agent()
    Data_Cleaner_task =Data_Cleaner.get_task()
    Data_Cleaner_task.description =cleaning_prompt.safe_substitute(working_dir=job_dir_path.as_posix())

    Data_Analyzer = DataAnalyzerAgent(cmd_tool)
    Data_Analyzer_Agent =Data_Analyzer.get_agent()
    Data_Analyzer_task =Data_Analyzer.get_task()
    Data_Analyzer_task.description =analysis_prompt.safe_substitute(working_dir=job_dir_path.as_posix())
    
    Data_Visualizer = DataVisualizerAgent(cmd_tool)
    Data_Visualizer_Agent =Data_Visualizer.get_agent()
    Data_Visualizer_task =Data_Visualizer.get_task()
    Data_Visualizer_task.description =visualizations_prompt.safe_substitute(working_dir=job_dir_path.as_posix())

    Report_Writer = ReportWriterAgent()
    Report_Writer_Agent =Report_Writer.get_agent()
    Report_Writer_task =Report_Writer.get_task()
    Report_Writer_task.description =report_writer_prompt.safe_substitute(working_dir=job_dir_path.as_posix(),report_md_path =final_md_path.as_posix())

    Translation =UniversalTranslationAgent()
    Translation_Agent =Translation.get_agent()
    Translation_task =Translation.get_task()


    Report_Generator = ReportGeneratorAgent(cmd_tool)
    Report_Generator_Agent =Report_Generator.get_agent()
    Report_Generator_task =Report_Generator.get_task()
    Report_Generator_task.description =Convert_md_to_pdf_prompt.safe_substitute(working_dir =job_dir_path.as_posix(),
                                                                                file_path=final_md_path.as_posix(),output_report=final_pdf_path.as_posix())

    SendEmail =ReportSenderAgent()
    SendEmail_Agent =SendEmail.get_agent()
    SendEmail_task =SendEmail.get_task()
    SendEmail_task.description =SendEmail_prompt.safe_substitute(working_dir=job_dir_path.as_posix(),file_path=final_pdf_path.as_posix(),
                                                                 managers=DataAnalysis_Request.MANAGER_EMAIL)

    if DataAnalysis_Request.Language== Languages.ARABIC.value: 
        Translation_task.description =Translation_prompt.safe_substitute(working_dir=job_dir_path.as_posix(),source_language=Languages.ENGLISH.value,
                                                                         target_language=Languages.ARABIC.value)
        crew = Crew(
                agents=[Data_Reader_Agent,
                        Data_Cleaner_Agent,
                        Data_Analyzer_Agent,
                        Data_Visualizer_Agent,
                        Report_Writer_Agent,
                        Translation_Agent,
                        Report_Generator_Agent,
                        SendEmail_Agent],

                tasks=[Data_Reader_task,
                        Data_Cleaner_task,
                        Data_Analyzer_task,
                        Data_Visualizer_task,
                        Report_Writer_task,
                        Translation_task,
                        Report_Generator_task,
                        SendEmail_task],          
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
        if os.path.exists(final_pdf_path):
            backgroudtask.add_task(shutil.rmtree, job_dir_path)
            return FileResponse(
                path=final_pdf_path.as_posix(),
                filename="Data_Analysis_Report.pdf",
                media_type='application/pdf',
                headers={
            "Content-Disposition": "inline; filename=Data_Analysis_Report.pdf"
                        }

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
    
    else:
         response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Agent not support this language"}

                                )
        

