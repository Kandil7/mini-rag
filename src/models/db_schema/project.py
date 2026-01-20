from pydantic import BaseModel ,Field ,field_validator
from typing import Optional
from bson.objectid import ObjectId
from pydantic import AliasChoices



class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id", validation_alias=AliasChoices('_id', 'id'))
    project_id: str = Field(..., min_length=1)

    #validate project id
    @field_validator('project_id')
    def vaildate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError('project id should be alphanumeric')
        return value

    class Config:
        arbitrary_types_allowed=True
        populate_by_name=True