from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_name: str
    env: str
    database_url: str

    
settings = Settings()