from fastapi import APIRouter, Depends

from app.schemas.muscle import MuscleRead
from app.api.dependencies import get_muscle_service
from app.services.muscle import MuscleService
from app.models.user import User
from app.core.auth import get_current_user


router = APIRouter(prefix="/muscles", tags=["muscles"])


@router.get("/", response_model=list[MuscleRead])
def list_muscles(
    service: MuscleService = Depends(get_muscle_service)
):
    return service.list_muscles()