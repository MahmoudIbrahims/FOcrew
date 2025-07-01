from sqlalchemy.orm import sessionmaker
from Controllers.BaseController import BaseController
from .DBProviders.PGDataBase import PGDataBaseProvider
from  .DataBaseEnums import DataBaseName

class DataBaseProviderFactory:
    def __init__(self, config, db_client: sessionmaker=None):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client

    def create(self, provider: str):
        
        if provider == DataBaseName.PGVECTOR.value:
            return PGDataBaseProvider(
                db_client=self.db_client,
            )
        
        return None