from fastapi import FastAPI , APIRouter,Depends, UploadFile
from helpers.config import get_settings,Settings
from controllers import DataController

data_router = APIRouter(
     prefix='/api/v1/data',
     tags=['data']
)

@data_router.post('/upload/{project_id}')

async def upload_data(project_id:str , file:UploadFile,
                      app_settings:Settings= Depends(get_settings)):
    
    #validate the file type and size
    is_validate= DataController().validate_uploud_file(file)
        

    return is_validate