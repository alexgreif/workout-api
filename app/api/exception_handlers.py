from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.domain.errors import (
    UserAlreadyExistsError,
    UserNotFoundError,
    ExerciseNotFoundError,
    InvalidMuscleError
)


def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User already exists"}
    )


def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"}
    )


def exercise_not_found_handler(
        request: Request,
        exc: ExerciseNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Exercise not found"}
    )


def invalid_muscle_handler(
        request: Request,
        exc: InvalidMuscleError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": "Invalid muscle IDs",
                 "missing_ids": sorted(exc.missing_ids)
        }
    )