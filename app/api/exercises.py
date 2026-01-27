from fastapi import APIRouter, Depends, status

from app.schemas.exercise import ExerciseCreate, ExerciseRead
from app.api.dependencies import get_exercise_service
from app.services.exercise import (
    ExerciseService
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
