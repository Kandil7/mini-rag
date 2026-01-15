from fastapi import FastAPI , APIRouter,Depends, UploadFile,status
from fastapi.responses import JSONResponse
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
    is_validate, response_signal = DataController().validate_upload_file(file)

    if not is_validate:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
             'message': response_signal
         }
       )   

    return {
        'response': response_signal ,
        
    }