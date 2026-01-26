from sqlalchemy.orm import Session

from app.models.exercise import Exercise
from app.models.muscle import Muscle
from app.models.exercise_muscle import ExerciseMuscle


class ExerciseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            exercise: Exercise
    ) -> Exercise:
        self.db.add(exercise)
        self.db.flush()
        return exercise
    
    def add_muscle(
            self,
            excercise_id: int,
            muscle_id: int,
            role: str
    ) -> None:
        link = ExerciseMuscle(
        excercise_id=excercise_id,
        muscle_id=muscle_id,
        role=role
        )
        self.db.add(link)
    

