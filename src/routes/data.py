from fastapi import FastAPI , APIRouter,Depends, UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import aiofiles 
from models import ResponseSignal
from controllers import DataController,ProjectController

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

    # return {
    #     'response': response_signal ,
        
    # }
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path=os.path.join(project_dir_path, file.filename)

    async with aiofiles.open(file_path, mode='wb') as f:
       while chunck := await file.read(app_settings.FILE_DEFUALT_CHANCK_SIZE):
         await f.write(chunck)

    return JSONResponse(
       content={
          'response': ResponseSignal.FILE_UPLOAD_SUCCESS.value
       }
    )