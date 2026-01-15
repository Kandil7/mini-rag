from fastapi import UploadFile
from .BaseController import BaseController

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 #convert MB to bytes


    def validate_uploud_file(self, file):
        # validate the file type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYEPE:
            raise False
        if file.size*self.size_scale > self.app_settings.FILE_MAX_SIZE:
            return False
        return True