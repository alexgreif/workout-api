from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.exercise import Exercise
from app.models.muscle import Muscle
from app.models.exercise_muscle import ExerciseMuscle


class ExerciseNotFoundError(Exception):
    pass


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
            exercise_id: int,
            muscle_id: int,
            role: str
    ) -> None:
        link = ExerciseMuscle(
            exercise_id=exercise_id,
            muscle_id=muscle_id,
            role=role
        )
        self.db.add(link)


    def get_by_id(self, exercise_id: int) -> Exercise | None:
        query = (
            select(Exercise)
            .options(
                selectinload(Exercise.muscles)
                .selectinload(ExerciseMuscle.muscle)
            )
            .where(Exercise.id == exercise_id)
        )

        exercise = self.db.execute(query).scalar_one_or_none()

        if exercise is None:
            raise ExerciseNotFoundError()
        
        return exercise


    def list_all(self) -> list[Exercise]:
        query = (
            select(Exercise)
            .options(
                selectinload(Exercise.muscles)
                .selectinload(ExerciseMuscle.muscle)
            )
        )

        return self.db.execute(query).scalars().all()


    

