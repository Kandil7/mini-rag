from .BaseController import BaseController
from .ProcessController import ProjectContorller
import os
from langchain_community.document_loader import TextLoader 
from langchain_community.document_loader import pyMuPDFLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter
from models.enums import ProcessingEnum
class ProcessController(BaseController):

    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectContorller().get_project_path(project_id=project_id)

    def get_file_extension(self,file_id:str):
        return os.path.splitText()[-1]
    def get_file_loader(self,file_id:str,file_path:str):

        file_ext=self.get_file_extension(file_id=file_id)

        if file_ext==ProcessingEnum.TXT.value:
            return TextLoader(file_path,encodin='utf-8')
        if file_ext==ProcessingEnum.PDF.value:
            return pyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def process_file_content(self,file_content:list,file_id:str,
                             chunck_size:int =100,overlap_size:int =20
                             ):

        text_spliter=RecursiveCharacterTextSplitter(
            chunck_size=chunck_size,
            chunck_overlap=overlap_size,
            length_function=len,



        )

        file_content_text=[

            rec.page
            for rec in file_content
        ]

        file_content_metedate=[
            rec.metadata
            for rec in file_content
        ]

        chuncks=text_spliter.create_documents(
            file_content_text,
            metadatas=file_content_metedate,

        )

        return chuncks
    
