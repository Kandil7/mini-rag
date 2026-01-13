from fastapi import FastAPI , APIRouter
from helpers.config import get_settings

base_router = APIRouter(
    # prefix='/',
    # tags=['Base']
)

@base_router.get('/')

def welcome():
    app_settings=get_settings()
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {'app_name': app_name, 'app_version': app_version}
 

