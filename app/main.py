from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router
from app.core.database import engine, Base


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(router)
    return app


app = create_app()
