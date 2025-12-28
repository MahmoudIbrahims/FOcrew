from .BaseDataModel import BaseDataModel
from .db_schemes.DBSchemas import UserFile
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy import desc 


class UserFileModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)

    async def create_user_file(self, user_file: UserFile):
        async with self.db_client() as session:
            async with session.begin():
                session.add(user_file)
            await session.commit()
            await session.refresh(user_file)
        return user_file

    async def get_file_or_create_one(
        self,
        file_uuid,
        original_filename,
        file_type,
        file_size,
        file_path,
        project_id
    ):
        async with self.db_client() as session:
            async with session.begin():
                query = select(UserFile).where(UserFile.file_uuid == file_uuid)
                result = await session.execute(query)
                user_file = result.scalar_one_or_none()

                if user_file is None:
                    new_file = UserFile(
                        file_uuid=file_uuid,
                        original_filename=original_filename,
                        file_type=file_type,
                        file_size=file_size,
                        file_path=file_path,
                        project_id=project_id
                    )
                    user_file = await self.create_user_file(new_file)

                return user_file

    async def get_all_files(self, page: int = 1, page_size: int = 10):
        async with self.db_client() as session:
            async with session.begin():
                count_query = await session.execute(
                    select(func.count(UserFile.file_id))
                )
                total_documents = count_query.scalar_one()

                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1

                query = select(UserFile).offset((page - 1) * page_size).limit(page_size)
                result = await session.execute(query)
                files = result.scalars().all()

                return files, total_pages
            
        

    async def get_latest_user_file_by_project(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                query = (
                    select(UserFile)
                    .where(UserFile.project_id == project_id)
                    .order_by(desc(UserFile.created_at))  
                    .limit(1)
                )
                result = await session.execute(query)
                user_file = result.scalar_one_or_none()
                return user_file

