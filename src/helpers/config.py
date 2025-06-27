from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    
    APP_NAME:str
    APP_VERSION: str
    
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:str
    POSTGRES_MAIN_DATABASE:str
    
    MODEL_NAME_LITERAL:List[str]=None
    MODEL_NAME:str
    API_KEY:str
    
    AGENT_NAME:str
    AGANT_NAME_LITERAL:List[str]=None
    DATA_PATH:str
    
    COMPANY_NAME:str
    INDUSTRY_NAME:str
    LANGUAGE_LITERAL:List[str]=None
    LANGUAGE:str
    
    
    
    class Config:
        env_file =".env"
        
    
def get_settings():
    return Settings()