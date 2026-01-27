from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import UserCreate, UserRead
from app.api.dependencies import get_user_service
from app.services.user import (
    UserService, UserAlreadyExistsError, UserNotFoundError
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
        "",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        )
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.register_user(
        email=payload.email,
        password=payload.password
    )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.get_user(user_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
