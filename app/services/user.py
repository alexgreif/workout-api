from sqlalchemy.orm import Session

from app.repositories.user import (
    UserRepository,
    UserAlreadyExistsError,
    UserNotFoundError
)
from app.models.user import User
from app.core.security import hash_password


class UserService:
    def __init__(self, db: Session, user_repo: UserRepository):
        self.db = db
        self.user_repo = user_repo

    def register_user(self, *, email: str, password: str) -> User:
        user = User(
            email=email,
            password_hash=hash_password(password)
        )

        try:
            self.user_repo.create(user=user)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return user
    
    def get_user(self, *, user_id: int) -> User:
        return self.user_repo.get_by_id(user_id)
