from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    APP_NAME : str
    APP_VERSION : str

    FILE_ALLOWED_TYPE: List[str]
    FILE_MAX_SIZE : int
    FILE_DEFUALT_CHANCK_SIZE:int

    MONGODB_URL : str
    MONGODB_DATABASE : str


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()