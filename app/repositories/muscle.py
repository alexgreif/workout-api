from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.muscle import Muscle


class MuscleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Muscle]:
        stmt = (select(Muscle).order_by(Muscle.name))
        return list(self.db.scalars(stmt))
    