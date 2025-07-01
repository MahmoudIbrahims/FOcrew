from fastapi import FastAPI
from routes import base,AgentsRouter
from helpers.config import get_settings
from Agents.AgentProviderFactory import AgentProviderFactory
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from Providers import DataBaseProviderFactory

app =FastAPI()


async def startup_span():
    settings = get_settings()
    postgres_conn =f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postgres_conn)
    
    app.db_client = sessionmaker(
        app.db_engine , class_ =AsyncSession, 
        expire_on_commit= False
        )

    Agent_provider_factory = AgentProviderFactory(settings.Config)
    app.Agent_client = Agent_provider_factory.create(Crew_Name=settings.AGENT_NAME,lanuage=settings.LANGUAGE,
                                                     file_path=settings.DATA_PATH)
    
    db_provider_factory = DataBaseProviderFactory(settings.Config ,db_client=app.db_client)
    app.Database_client =db_provider_factory.create(
                         provider=settings.DB_BACKEND
        
                                )
    
    
async def shutdown_span():
    app.db_engine.dispose()
    


app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(AgentsRouter.agent_router)

