from fastapi import FastAPI
from routes import base,data
from helpers.config import Settings,get_settings
from motor.motor_asyncio import AsyncIOMototClient

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMototClient(Settings.MONGODB_URL)
    app.db = app.mongodb_client[Settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(base.base_router)
app.include_router(data.data_router)
