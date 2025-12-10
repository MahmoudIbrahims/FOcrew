from pydantic_settings import BaseSettings
from typing import List,Optional

class Settings(BaseSettings):
    
    APP_NAME:str
    APP_VERSION: str
    
    FILE_ALLOWED_TYPES:List[str]
    DB_BACKEND:str
    
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_PORT:str
    POSTGRES_MAIN_DATABASE:str

    SUPABASE_URL:str =None
    SUPABASE_SECRET:str =None

    ENDPOINT_URL:str
    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str
    REGION:str
    AWS_BUCKET:str

    MODEL_NAME_LITERAL:List[str]=None
    MODEL_NAME:str
    API_KEY:str
    TEMPERATURE:float

    BEAM_ENDPOINT:str
    BEAM_AUTH_TOKEN:str
    TEMPERATURE_BEAM:float

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