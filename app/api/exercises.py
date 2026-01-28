from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.exercise import ExerciseCreate, ExerciseRead
from app.api.dependencies import get_exercise_service
from app.services.exercise import (
    ExerciseService, ExerciseNotFoundError
)


router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post(
        "",
        response_model=ExerciseRead,
        status_code=status.HTTP_201_CREATED,
        )
def create_exercise(
    payload: ExerciseCreate,
    service: ExerciseService = Depends(get_exercise_service),
):
    return service.add_exercise(
        name=payload.name,
        description=payload.description,
        created_by_user_id=1,
        muscles=[(m.muscle_id, m.role) for m in payload.muscles]
    )


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    service: ExerciseService = Depends(get_exercise_service)
    ):
    try:
        return service.get_exercise(exercise_id=exercise_id)
    except ExerciseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
