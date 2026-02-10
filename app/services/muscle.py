from sqlalchemy.orm import Session

from app.repositories.muscle import MuscleRepository
from app.models.muscle import Muscle


class MuscleService:
    def __init__(self, db: Session, muscle_repo: MuscleRepository):
        self.db = db
        self.muscle_repo = muscle_repo
    
    def list_muscles(self) -> list[Muscle]:
        return self.muscle_repo.list_all()
    