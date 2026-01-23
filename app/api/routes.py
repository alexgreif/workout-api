from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post(
        "/users",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        )
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(user)

    try:
        db.flush()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    
    return user


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}
