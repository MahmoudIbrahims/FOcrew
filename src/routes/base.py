from fastapi import FastAPI, APIRouter ,Depends
from helpers.config import get_settings ,Settings
import os 

base_router = APIRouter(
    prefix ="/health/v1",
    tags =["health_v1"],
)

@base_router.get('/')
async def welcome(app_settings:Settings =Depends(get_settings)):

    App_name = app_settings.APP_NAME
    App_version = app_settings.APP_VERSION

    return {
        "App_name": App_name,
        "App_version": App_version,

    }