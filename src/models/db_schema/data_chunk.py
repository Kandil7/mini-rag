from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from pydantic import AliasChoices

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id", validation_alias=AliasChoices('_id', 'id'))
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId = Field(...)
    chunk_asset_id: ObjectId


    class Config:
        arbitrary_types_allowed=True
        populate_by_name=True
        json_encoder={
            ObjectId:str
        }
    @classmethod
    def get_indexes(cls):
        return[{
            "key":[("chunk_project_id",1)

            ],
            "name":"chunk_project_index_1",
            "unique":False
        }]