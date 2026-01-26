from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env.app")

    app_name: str
    env: str
    database_url: str

    
settings = Settings()