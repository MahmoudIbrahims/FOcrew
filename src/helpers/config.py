from pydantic_settings import BaseSettings
from typing import List,Optional

class Settings(BaseSettings):
    
    APP_NAME:str="FOcrew"
    APP_VERSION: str="0.1"
    
    FILE_ALLOWED_TYPES:List[str]
    DB_BACKEND:str
    
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:str
    POSTGRES_MAIN_DATABASE:str
    
    MODEL_NAME_LITERAL:List[str]=None
    MODEL_NAME:str
    API_KEY:str
    TEMPERATURE:float
    
    AGENT_NAME:str
    AGANT_NAME_LITERAL:List[str]=None
    DATA_PATH:Optional[str] = None
    
    COMPANY_NAME:str
    INDUSTRY_NAME:str
    LANGUAGE_LITERAL:List[str]=None
    LANGUAGE:str
    LOGO_COMPANY:str=None
    
    GMAIL_USER:str
    GMAIL_APP_PASSWORD:str
    MANAGER_LITERAL:List[str]=None
    MANAGERS: str
    
    class Config:
        env_file =".env"
        
    
def get_settings():
    return Settings()