from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router
from app.api.health import router as health_router
from app.api.exception_handlers import (
    user_already_exists_handler,
    user_not_found_handler,
    exercise_not_found_handler,
    invalid_muscle_handler
)
from app.domain.errors import (
    UserAlreadyExistsError,
    UserNotFoundError,
    ExerciseNotFoundError,
    InvalidMuscleError
)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    # Exception handlers
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(ExerciseNotFoundError, exercise_not_found_handler)
    app.add_exception_handler(InvalidMuscleError, invalid_muscle_handler)

    # Routers
    app.include_router(api_router)
    app.include_router(health_router)
    return app


app = create_app()
