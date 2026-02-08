from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str
    database_url: str
    secret_key: str

    
settings = Settings()