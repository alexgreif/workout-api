from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserRead

from app.repositories.user import (
    UserRepository, UserAlreadyExistsError, UserNotFoundError
)
from app.api.dependencies import get_user_repository

router = APIRouter()


@router.post(
        "/users",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        )
def create_user(
    payload: UserCreate,
    repo: UserRepository = Depends(get_user_repository),
):
    try:
        user = repo.create(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    
    return user


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    try:
        return repo.get_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}
