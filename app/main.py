from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router
from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)
    app.include_router(health_router)
    return app


app = create_app()
