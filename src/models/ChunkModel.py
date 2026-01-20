from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schema.data_chunk import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne
class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client=db_client)
        self.collection =self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self,chunk:DataChunk):
        result=await self.collection.insert_one({
            "id":chunk.id
        })
        chunk.id=result.inserted_id

        return chunk
    
    async def get_chunk(self,chunk_id:str):
        record=await self.collection.find_one({
            "id":ObjectId(chunk_id)
        })

        if record is None:
            return None
        
        return DataChunk(**record)
    async def insert_many_chunks(self,chunks:list,batch_size:int=100):
        
        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]

            operations=[
                InsertOne(chunk.dict())
                for chunk in batch
            ]

            return self.collection.bulk_write(operations)
        return len(chunks)
