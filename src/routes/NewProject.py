from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from Models.ProjectModel import ProjectModel
from .Schemes.Newproject import ProjectCreateRequest
from .Enums.NewprojectEnums import NewprojectEnums
import logging

logger = logging.getLogger('uvicorn.error')

project_router = APIRouter(
    prefix="/api/v1/project",
    tags=["api_v1", "project"],
)


@project_router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_project(
    request: Request, 
    project_data: ProjectCreateRequest
    ):

    """Create a new project"""
    try:
        model = await ProjectModel.create_instance(db_client=request.app.db_client)
        project = await model.create_new_project(
            project_name=project_data.project_name,
            company_name=project_data.company_name,
            industry_name=project_data.industry_name,
            report_language=project_data.report_language,
            manager_email=project_data.manager_email
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": NewprojectEnums.PROJECT_CREATE_SUCCESSFULLY.value,
                "project_id": str(project.project_id),
                "project_name": project.project_name
            }
        )
    
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": f"Failed to create project: {str(e)}"
                })


@project_router.get('/{project_id}')
async def get_project(request: Request, project_id: str):
    """Get project by ID"""
    try:
        model = await ProjectModel.create_instance(db_client=request.app.db_client)
        project = await model.get_project_by_id(project_id)
        
        if not project:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":NewprojectEnums.PROJECT_NOT_FOUND.value}
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "project_id": str(project.project_id),
                "project_name": project.project_name,
                "company_name": project.company_name,
                "industry_name": project.industry_name,
                "report_language": project.report_language,
                "manager_email": project.manager_email,
                "created_at": project.created_at.isoformat() if project.created_at else None
            }
        )
    
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Failed to get project: {str(e)}"}
        )


@project_router.get('/list/all')
async def list_projects(request: Request, page: int = 1, page_size: int = 10):
    """Get all projects with pagination"""
    try:
        model = await ProjectModel.create_instance(db_client=request.app.db_client)
        projects, total_pages = await model.get_all_projects(page=page, page_size=page_size)
        
        projects_list = [
            {
                "project_id": str(p.project_id),
                "project_name": p.project_name,
                "company_name": p.company_name,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in projects
        ]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "projects": projects_list,
                "page": page,
                "total_pages": total_pages
            }
        )
    
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Failed to list projects: {str(e)}"}
        )


@project_router.delete('/{project_id}')
async def delete_project(request: Request, project_id: str):
    """Delete a project"""
    try:
        model = await ProjectModel.create_instance(db_client=request.app.db_client)
        deleted = await model.delete_project(project_id)
        
        if not deleted:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": NewprojectEnums.PROJECT_NOT_FOUND.value}
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": NewprojectEnums.PROJECT_DELETED_SUCCESSFULLY.value}
        )
    
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Failed to delete project: {str(e)}"}
        )