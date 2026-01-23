from app.repositories.user import (
    UserRepository,
    UserAlreadyExistsError,
    UserNotFoundError
)
from app.models.user import User
from app.core.security import hash_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, *, email: str, password: str) -> User:
        password_hash=hash_password(password)

        return self.user_repo.create(
            email=email,
            password_hash=password_hash
            )
    
    def get_user(self, *, user_id: int) -> User:
        return self.user_repo.get_by_id(user_id)
