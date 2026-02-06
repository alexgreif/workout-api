from fastapi import APIRouter, Depends, status

from app.schemas.exercise import ExerciseCreate, ExerciseRead
from app.api.dependencies import get_exercise_service
from app.services.exercise import ExerciseService
from app.models.user import User
from app.core.auth import get_current_user


router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post(
        "",
        response_model=ExerciseRead,
        status_code=status.HTTP_201_CREATED,
        )
def create_exercise(
    payload: ExerciseCreate,
    service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(get_current_user)
):
    return service.add_exercise(
        name=payload.name,
        description=payload.description,
        created_by_user_id=user.id,
        muscles=[(m.muscle_id, m.role) for m in payload.muscles]
    )


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(get_current_user)
):
    return service.get_exercise(exercise_id=exercise_id, user=user)


@router.get("/", response_model=list[ExerciseRead])
def list_exercises(
    service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(get_current_user)
):
    return service.list_exercises(user=user)