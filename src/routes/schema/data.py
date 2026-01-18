from pydantic import BaseModel 
from typing import Optional

class ProcessRequest(BaseModel):
    fild_id:str
    chunck_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_rest: Optional[int] = 0