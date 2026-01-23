from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.db.add(user)

        try:
            self.db.flush()
        except IntegrityError:
            raise UserAlreadyExistsError()
        
        return user
    
    def get_by_id(self, user_id: int) -> User:
        user = self.db.get(User, user_id)

        if user is None:
            raise UserNotFoundError()
        
        return user