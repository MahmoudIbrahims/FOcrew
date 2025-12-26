from fastapi import APIRouter, Depends, UploadFile, status, Request, HTTPException, File
from Controllers.DataController import DataController
from Models.enums.ResponseEnum import ResponseSignal
from helpers.config import get_settings, Settings
from Models.UserFileModel import UserFileModel
from fastapi.responses import JSONResponse
from Models.ProjectModel import ProjectModel
from Models.schema.DBSchemas import UserFile
from .Enums.BasicsEnums import FileNameEnum
import pandas as pd
from io import BytesIO
from datetime import datetime
from pandas import Timestamp
import logging
import numpy as np
import tempfile 
import uuid
import os


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

def convert_to_json_serializable(obj):
    if isinstance(obj, (datetime, Timestamp)):
        return obj.isoformat()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

@data_router.post('/upload/{project_id}')
async def upload_data(request: Request, project_id: str, file: UploadFile = File(...),
                      app_settings: Settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_by_id(project_id)

    # 1. Validate the file
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal},
        )
    
    file_uuid = uuid.uuid4()
    file_extension = file.filename.split(".")[-1].lower()
    
    # 2. Read file content once
    contents = await file.read()
    file_size = len(contents)

    try:
        # Read content into Pandas using an in-memory stream (BytesIO)
        if file_extension == FileNameEnum.CSV.value:
            df = pd.read_csv(BytesIO(contents),encoding="latin1")
        elif file_extension in [FileNameEnum.EXCEL.value, FileNameEnum.SHEET.value]:
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # 3. Prepare S3 Key
        # S3 Key = [Project Prefix] / [UUID] . [Extension]
        s3_prefix = data_controller.get_database_key_prefix(f"project_{project_id}")
        s3_key = f"{s3_prefix}/{file_uuid}.{file_extension}"
        
        # 4. Save to temporary local path and then upload to S3
        temp_file_path = None
        try:
            # Create a temporary local file for the S3 upload process
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(contents)
                temp_file_path = tmp_file.name
                
            # Upload to S3 using the temporary path
            data_controller.upload_file_to_s3_only(
                local_file_path=temp_file_path,
                s3_key=s3_key
            )
            
        finally:
            # 🗑️ Ensure the temporary file is deleted, regardless of success or failure
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
        # 5. Process data for database schema
        df = df.replace({np.nan: None})
        rows_count = df.shape[0]
        columns_count = df.shape[1]

        columns_info = df.dtypes.apply(lambda x: str(x)).to_dict()
        sample_data = [
            {k: convert_to_json_serializable(v) for k, v in record.items()}
            for record in df.head(5).to_dict(orient="records")
        ]

        # 6. Save metadata to the database using the S3 Key
        user_file = UserFile(
            file_uuid=file_uuid,
            original_filename=file.filename,
            file_type=file_extension,
            file_size=file_size,
            file_path=s3_key,  
            rows_count=rows_count,
            columns_count=columns_count,
            columns_info=columns_info,
            sample_data=sample_data,
            is_processed=False,
            processing_status="uploaded",
            project_id=project_id
        )

        model = await UserFileModel.create_instance(db_client=request.app.db_client)
        saved_file = await model.create_user_file(user_file)

        return JSONResponse(
            content={
                "message": ResponseSignal.FILE_UPLOADED_Success.value,
                "file_id": str(saved_file.file_id),
                "original_filename": str(saved_file.original_filename),
                "file_size": file_size,
                "rows": rows_count,
                "columns": columns_count,
                
            }
        )

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        # Secondary cleanup check in case the exception happened before the finally block was entered 
        # (though less likely in this structure, it's good practice for safety)
        if 'temp_file_path' in locals() and temp_file_path and os.path.exists(temp_file_path):
             os.unlink(temp_file_path)
             
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOADED_FAILED.value,
                "error": str(e)
            }
        )