from fastapi import UploadFile
from .BaseController import BaseController

from models import ResponseSignal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 #convert MB to bytes


    def validate_upload_file(self, file: UploadFile):
        # validate the file type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False , ResponseSignal.INVALID_FILE_TYPE.value
        # file.size is in bytes, FILE_MAX_SIZE is in MB, so convert MB to bytes for comparison
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False , ResponseSignal.INVALID_FILE_SIZE.value
        # upload the file successfully
        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value
