from .BaseController import BaseController
from .ProcessController import ProjectContorller
import os
from langchain_community.document_loader import TextLoader 
from langchain_community.document_loader import pyMuPDFLoader

class ProcessController(BaseController):

    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectContorller().get_project_path(project_id=project_id)

    def get_file_extension(self,file_id:str):
        os.path.splitText()[-1]

    
