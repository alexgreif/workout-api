from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.domain.errors import UserAlreadyExistsError, UserNotFoundError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, user: User) -> User:
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