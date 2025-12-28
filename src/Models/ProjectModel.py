from .BaseDataModel import BaseDataModel
from .db_schemes.DBSchemas import Project
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional
import uuid


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client
    
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance
    

    async def create_project(self, project: Project):
        """Create a new project"""
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
        return project

    async def create_new_project(
        self,
        project_name: str,
        company_name: Optional[str] = None,
        industry_name: Optional[str] = None,
        report_language: str = "Arabic",
        manager_email: Optional[str] = None
    ):
        """Create a new project with data"""
        project = Project(
            project_name=project_name,
            company_name=company_name,
            industry_name=industry_name,
            report_language=report_language,
            manager_email=manager_email
        )
        return await self.create_project(project)

    async def get_project_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        """Get project by ID"""
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
        return project

    async def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """Get project by name"""
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_name == project_name)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
        return project

    async def update_project(
        self,
        project_id: uuid.UUID,
        project_name: Optional[str] = None,
        company_name: Optional[str] = None,
        industry_name: Optional[str] = None,
        report_language: Optional[str] = None,
        manager_email: Optional[str] = None
    ) -> Optional[Project]:
        """Update project data"""
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                
                if project is None:
                    return None
                
                if project_name is not None:
                    project.project_name = project_name
                if company_name is not None:
                    project.company_name = company_name
                if industry_name is not None:
                    project.industry_name = industry_name
                if report_language is not None:
                    project.report_language = report_language
                if manager_email is not None:
                    project.manager_email = manager_email
                    
            await session.commit()
            await session.refresh(project)
        return project

    async def delete_project(self, project_id: uuid.UUID) -> bool:
        """Delete a project"""
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                
                if project is None:
                    return False
                
                await session.delete(project)
            await session.commit()
        return True

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """Get all projects with pagination"""
        async with self.db_client() as session:
            async with session.begin():
                # Calculate total count
                total_query = select(func.count(Project.project_id))
                total_result = await session.execute(total_query)
                total_documents = total_result.scalar_one()
                
                # Calculate total pages
                total_pages = (total_documents + page_size - 1) // page_size
                
                # Fetch projects
                query = select(Project).offset((page - 1) * page_size).limit(page_size)
                result = await session.execute(query)
                projects = result.scalars().all()
                
        return projects, total_pages

    async def check_project_exists(self, project_id: uuid.UUID) -> bool:
        """Check if project exists"""
        project = await self.get_project_by_id(project_id)
        return project is not None