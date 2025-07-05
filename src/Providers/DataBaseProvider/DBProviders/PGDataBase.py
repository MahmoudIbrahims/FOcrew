from ..DataBaseInterface import DataBaseInterface
import logging
from typing import List
from sqlalchemy.sql import text as sql_text
import json

class PGDataBaseProvider(DataBaseInterface):

    def __init__(self, db_client):
        self.db_client = db_client
        self.logger = logging.getLogger("uvicorn")

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def is_collection_existed(self, collection_name: str) -> bool:
        async with self.db_client() as session:
            async with session.begin():
                query = sql_text('SELECT 1 FROM pg_tables WHERE tablename = :collection_name')
                result = await session.execute(query, {"collection_name": collection_name})
                return result.scalar_one_or_none() is not None

    async def list_all_collections(self) -> List[str]:
        async with self.db_client() as session:
            async with session.begin():
                query = sql_text('SELECT tablename FROM pg_tables')
                result = await session.execute(query)
                return result.scalars().all()

    async def create_collection(self, collection_name: str, do_reset: bool = False):
        if do_reset:
            await self.delete_collection(collection_name)

        if not await self.is_collection_existed(collection_name):
            async with self.db_client() as session:
                async with session.begin():
                    create_sql = sql_text(f'''
                        CREATE TABLE {collection_name} (
                            id bigserial PRIMARY KEY,
                            text TEXT,
                            metadata JSONB DEFAULT '{{}}'
                        )
                    ''')
                    await session.execute(create_sql)
            return True
        return False

    async def delete_collection(self, collection_name: str):
        async with self.db_client() as session:
            async with session.begin():
                await session.execute(sql_text(f'DROP TABLE IF EXISTS {collection_name}'))
        return True

    async def insert_one(self, collection_name: str, text: str, metadata: dict = None):
        if not await self.is_collection_existed(collection_name):
            self.logger.error(f"Collection does not exist: {collection_name}")
            return False

        metadata_json = json.dumps(metadata or {}, ensure_ascii=False)
        async with self.db_client() as session:
            async with session.begin():
                query = sql_text(f'''
                    INSERT INTO {collection_name} (text, metadata)
                    VALUES (:text, :metadata)
                ''')
                await session.execute(query, {
                    "text": text,
                    "metadata": metadata_json
                })
        return True

    async def insert_many(self, collection_name: str, texts: list, metadata: list = None):
        if not await self.is_collection_existed(collection_name):
            self.logger.error(f"Collection does not exist: {collection_name}")
            return False

        metadata = metadata or [{}] * len(texts)

        async with self.db_client() as session:
            async with session.begin():
                query = sql_text(f'''
                    INSERT INTO {collection_name} (text, metadata)
                    VALUES (:text, :metadata)
                ''')
                for t, m in zip(texts, metadata):
                    await session.execute(query, {
                        "text": t,
                        "metadata": json.dumps(m, ensure_ascii=False)
                    })
        return True

    async def get_collection_info(self, collection_name: str) -> dict:
        if not await self.is_collection_existed(collection_name):
            return None

        async with self.db_client() as session:
            async with session.begin():
                count_sql = sql_text(f'SELECT COUNT(*) FROM {collection_name}')
                result = await session.execute(count_sql)
                count = result.scalar_one()
        return {"record_count": count}
