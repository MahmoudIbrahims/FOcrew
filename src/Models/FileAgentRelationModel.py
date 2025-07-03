from .BaseDataModel import BaseDataModel
from .schema.DBSchemas import FileAgentRelation
from sqlalchemy.future import select
from sqlalchemy import func


class FileAgentRelationModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)

    async def create_file_agent_relation(self, relation: FileAgentRelation):
        async with self.db_client() as session:
            async with session.begin():
                session.add(relation)
            await session.commit()
            await session.refresh(relation)
        return relation

    async def get_relation_or_create_one(
        self, file_id: int, agent_result_id: int, usage_type: str
    ):
        async with self.db_client() as session:
            async with session.begin():
                query = select(FileAgentRelation).where(
                    FileAgentRelation.file_id == file_id,
                    FileAgentRelation.agent_result_id == agent_result_id,
                    FileAgentRelation.usage_type == usage_type,
                )
                result = await session.execute(query)
                relation = result.scalar_one_or_none()

                if relation is None:
                    new_relation = FileAgentRelation(
                        file_id=file_id,
                        agent_result_id=agent_result_id,
                        usage_type=usage_type
                    )
                    relation = await self.create_file_agent_relation(new_relation)
                
                return relation

    async def get_all_relations(self, page: int = 1, page_size: int = 10):
        async with self.db_client() as session:
            async with session.begin():
                count_query = await session.execute(
                    select(func.count(FileAgentRelation.relation_id))
                )
                total_documents = count_query.scalar_one()

                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1

                query = select(FileAgentRelation).offset((page - 1) * page_size).limit(page_size)
                result = await session.execute(query)
                relations = result.scalars().all()

                return relations, total_pages
