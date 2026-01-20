from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from pydantic import AliasChoices

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id", validation_alias=AliasChoices('_id', 'id'))
    chunk_id: str = Field(..., min_length=1)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId = Field(..., min_length=1)


    class Config:
        arbitrary_types_allowed=True
        populate_by_name=True