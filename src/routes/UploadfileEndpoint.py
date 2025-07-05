from fastapi import APIRouter ,Depends,UploadFile,status,Request,HTTPException
from Models.UserFileModel import UserFileModel
from Models.ProjectModel import ProjectModel
from Controllers.DataController import DataController,ProjectController
from Models.schema.DBSchemas import UserFile
from helpers.config import get_settings ,Settings
from Models.enums.ResponseEnum import ResponseSignal
from fastapi.responses import JSONResponse
from .AGRouterEnums import FileNameEnum
import uuid
import pandas as pd
from io import StringIO,BytesIO
import logging
from fastapi import File


logger =logging.getLogger('uvcorn.error')

data_router = APIRouter(
    prefix ="/api/v1/data",
    tags =["api_v1","data"],
)

@data_router.post('/upload/{project_id}')
async def upload_data(request : Request ,project_id:int ,file : UploadFile = File(...),
                   app_settings:Settings =Depends(get_settings)):

    project_model = await ProjectModel.create_instance( 
        db_client = request.app.db_client
        
    )
    
    project =await project_model.get_project_or_create_one(
        project_id = project_id
    )
    
    
    data_controller = DataController()
    # validate the file properties
    is_valid, result_signal = data_controller.validate_uploaded_file(file =file)

    if not is_valid :
        return JSONResponse(
                status_code =status.HTTP_400_BAD_REQUEST,
                content ={
                    "signal" : result_signal
                },
        )
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path,file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    

    try:
        contents = await file.read()
        filename = file.filename
        file_type = filename.split(".")[-1].lower()
        file_size = len(contents)
        file_path = f"/virtual/path/{uuid.uuid4()}" 

      
        if file_type ==FileNameEnum.CSV.value:
            df = pd.read_csv(StringIO(contents.decode("utf-8")))
        elif file_type == FileNameEnum.EXCEL.value or FileNameEnum.SHEET.value:
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        rows_count = df.shape[0]
        columns_count = df.shape[1]
        columns_info = df.dtypes.apply(lambda x: str(x)).to_dict()
        sample_data = df.head(5).to_dict(orient="records")
        full_data = df.to_dict(orient="records")

       
        user_file = UserFile(
            file_uuid=uuid.uuid4(),
            original_filename=filename,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            rows_count=rows_count,
            columns_count=columns_count,
            columns_info=columns_info,
            sample_data=sample_data,
            full_data=full_data,
            storage_method="database",
            is_processed=False,
            processing_status="uploaded",
            project_id=project_id
        )

        model = await UserFileModel.create_instance(
            db_client = request.app.db_client)
        
        saved_file = await model.create_user_file(user_file)
        
        
        return JSONResponse(
                content ={
                    "message" : ResponseSignal.FILE_UPLOADED_Success.value,
                    "file_id" : str(saved_file.file_id),
                    "original_filename":str(saved_file.original_filename),
                    "rows":str(rows_count),
                    "columns": str(columns_count)
                    
                    
                }
        )
    

    except Exception as e:
        logger.error(f"Error while uploding file : {e}")
        return JSONResponse(
            status_code =status.HTTP_400_BAD_REQUEST,
            content ={
                "message" : ResponseSignal.FILE_UPLOADED_FAILED.value
            }
        )

