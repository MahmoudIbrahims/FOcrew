from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
class Settings(BaseSettings):
    
    APP_NAME:str
    APP_VERSION: str
    
    MODEL_NAME:str
    API_KEY:str
    
    AGENT_NAME:str
    COMPANY_NAME:str
    INDUSTRY_NAME:str
    LANGUAGE:str
    
    
    
    class Config:
        env_file =".env"
        
    
def get_settings():
    return Settings()