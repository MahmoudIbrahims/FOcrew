from fastapi import APIRouter, Depends, UploadFile, status, Request, HTTPException, File
from fastapi.responses import JSONResponse
from Models.UserFileModel import UserFileModel
from Models.ProjectModel import ProjectModel
from Controllers.DataController import DataController, ProjectController
from Models.schema.DBSchemas import UserFile
from helpers.config import get_settings, Settings
from Models.enums.ResponseEnum import ResponseSignal
from .Enums.BasicsEnums import FileNameEnum
import uuid
import pandas as pd
from io import BytesIO
import logging
import os
import numpy as np
from datetime import datetime
from pandas import Timestamp

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
async def upload_data(request: Request, project_id: int, file: UploadFile = File(...),
                     app_settings: Settings = Depends(get_settings)):

    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal},
        )

   
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    os.makedirs(project_dir_path, exist_ok=True)

    file_uuid = uuid.uuid4()
    file_extension = file.filename.split(".")[-1].lower()
    file_name = f"{file_uuid}.{file_extension}"
    file_path = os.path.join(project_dir_path, file_name)

    try:
        contents = await file.read()
        file_size = len(contents)

       
        with open(file_path, "wb") as f:
            f.write(contents)

        if file_extension == FileNameEnum.CSV.value:
            df = pd.read_csv(BytesIO(contents))
        elif file_extension in [FileNameEnum.EXCEL.value, FileNameEnum.SHEET.value]:
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        df = df.replace({np.nan: None})
        rows_count = df.shape[0]
        columns_count = df.shape[1]

        columns_info = df.dtypes.apply(lambda x: str(x)).to_dict()
        sample_data = [
            {k: convert_to_json_serializable(v) for k, v in record.items()}
            for record in df.head(5).to_dict(orient="records")
        ]

        user_file = UserFile(
            file_uuid=file_uuid,
            original_filename=file.filename,
            file_type=file_extension,
            file_size=file_size,
            file_path=file_path,  
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
                "file_uuid": str(file_uuid),
                "original_filename": str(saved_file.original_filename),
                "file_size": file_size,
                "rows": rows_count,
                "columns": columns_count,
                "file_path": file_path
            }
        )

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": ResponseSignal.FILE_UPLOADED_FAILED.value,
                "error": str(e)
            }
        )
