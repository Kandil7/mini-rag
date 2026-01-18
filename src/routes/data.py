from fastapi import FastAPI , APIRouter,Depends, UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import aiofiles 
from models import ResponseSignal
from controllers import DataController,ProjectController
from schema.data import ProcessRequest
import os
import logging

logger=logging.getLogger('uvicorn.error')

data_router = APIRouter(
     prefix='/api/v1/data',
     tags=['data']
)

@data_router.post('/upload/{project_id}')

async def upload_data(project_id:str , file:UploadFile,
                      app_settings:Settings= Depends(get_settings)):
    
    #validate the file type and size
    data_controller=DataController()
    is_validate, response_signal = data_controller.validate_upload_file(file)

    if not is_validate:
      return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
             'message': response_signal
         }
       )   

   
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path,file_id=data_controller.generate_unique_filepath(
        orig_file_name= file.filename,
         project_id=project_id
    )
    try:
        async with aiofiles.open(file_path, mode='wb') as f:
            while chunck := await file.read(app_settings.FILE_DEFUALT_CHANCK_SIZE):
                await f.write(chunck)
    except Exception as e:
         logger(f'Error uploading file: {e}')
         return JSONResponse(
         status_code=status.HTTP_400_BAD_REQUEST,
         content={
             'message': ResponseSignal.FILE_UPLOAD_FAILED.value
         }
       ) 

    return JSONResponse(
       content={
          'response': ResponseSignal.FILE_UPLOAD_SUCCESS.value,
          'file_id': file_id
       }
    )
@data_router.Post('/process/{project_id}')
async def process_endpoint(project_id: str, process_request: ProcessRequest):

    file_id=ProcessRequest.file_id
    
    return file_id

    # Process the file using the provided parameters
   