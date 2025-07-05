from .BaseDataModel import BaseDataModel
from .schema.DBSchemas import AgentResult
from sqlalchemy.future import select
from sqlalchemy import func


class AgentResultModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)

    async def create_agent_result(self, result: AgentResult):
        async with self.db_client() as session:
            async with session.begin():
                session.add(result)
            await session.commit()
            await session.refresh(result)
        return result

    async def get_result_or_create_one(
        self,
        result_uuid,
        agent_name,
        agent_type,
        project_id,
        result_data=None,
        result_text=None,
        status="completed"
    ):
        async with self.db_client() as session:
            async with session.begin():
                query = select(AgentResult).where(AgentResult.result_uuid == result_uuid)
                result = await session.execute(query)
                agent_result = result.scalar_one_or_none()

                if agent_result is None:
                    new_result = AgentResult(
                        result_uuid=result_uuid,
                        agent_name=agent_name,
                        agent_type=agent_type,
                        project_id=project_id,
                        result_data=result_data,
                        result_text=result_text,
                        status=status
                    )
                    agent_result = await self.create_agent_result(new_result)

                return agent_result

    async def get_all_results(self, page: int = 1, page_size: int = 10):
        async with self.db_client() as session:
            async with session.begin():
                count_query = await session.execute(
                    select(func.count(AgentResult.result_id))
                )
                total_documents = count_query.scalar_one()

                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1

                query = select(AgentResult).offset((page - 1) * page_size).limit(page_size)
                result = await session.execute(query)
                agent_results = result.scalars().all()

                return agent_results, total_pages
