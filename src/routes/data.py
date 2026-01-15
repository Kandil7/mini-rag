from fastapi import FastAPI , APIRouter,Depends,uploadFile
from helpers.config import get_settings,Settings

data_router = APIRouter(
     prefix='/api/v1/data',
     tags=['data']
)

@data_router.post('/upload/{project_id}')

async def upload_data(project_id:str , file:uploadFile,
                      app_settings:Settings= Depends(get_settings)):
    
    #validate the file type and size

    pass