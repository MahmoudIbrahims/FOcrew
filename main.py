from fastapi import FastAPI
from routes import base
from helpers.config import get_settings
from Agents.AgentProviderFactory import AgentProviderFactory

app =FastAPI()


async def startup_span():
    settings = get_settings()

    Agent_provider_factory = AgentProviderFactory(settings.Config)
    app.Agent_client = Agent_provider_factory.create(Crew_Name=settings.AGENT_NAME,lanuage=settings.LANGUAGE,
                                                     file_path=settings.DATA_PATH)
    
async def shutdown_span():
    pass
    


app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)


