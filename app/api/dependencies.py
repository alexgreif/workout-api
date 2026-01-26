from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.repositories.exercise import ExerciseRepository
from app.services.exercise import ExerciseService


def get_user_repository(
        db: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(db)


def get_user_service(
        db: Session = Depends(get_db),
        user_repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(db, user_repo)


def get_exercise_repository(
        db: Session = Depends(get_db)
) -> ExerciseRepository:
    return ExerciseRepository(db)


def get_exercise_service(
        db: Session = Depends(get_db),
        exercise_repo: UserRepository = Depends(get_exercise_repository)
) -> ExerciseService:
    return ExerciseService(db, exercise_repo)