from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id=Optional[ObjectId]
    chunk_id:str =Field(...,min_length=1)
    chunck_text:str =Field(...,min_length=1)
    chunk_metadata:dict =Field(...,min_length=1)
    chunck_order:int =Field(...,min_length=1)

    project_id:ObjectId=Field(...,min_length=1)


    class Config:
        arbitrary_types_allowed=True