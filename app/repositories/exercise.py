from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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
            exercise_id: int,
            muscle_id: int,
            role: str
    ) -> None:
        exercise_muscle = ExerciseMuscle(
            exercise_id=exercise_id,
            muscle_id=muscle_id,
            role=role
        )
        self.db.add(exercise_muscle)


    def add_muscles(
            self,
            exercise_id: int,
            muscles: list[tuple[int, str]]
    ) -> None:
        rows = [
            ExerciseMuscle(
                exercise_id=exercise_id,
                muscle_id=muscle_id,
                role=role
            )
            for muscle_id, role in muscles
        ]
        self.db.add_all(rows)


    def get_by_id(self, exercise_id: int) -> Exercise | None:
        stmt = (
            select(Exercise)
            .options(
                selectinload(Exercise.muscles)
                .selectinload(ExerciseMuscle.muscle)
            )
            .where(Exercise.id == exercise_id)
        )

        return self.db.execute(stmt).scalar_one_or_none()


    def list_all(self) -> list[Exercise]:
        stmt = (
            select(Exercise)
            .options(
                selectinload(Exercise.muscles)
                .selectinload(ExerciseMuscle.muscle)
            )
        )

        return self.db.execute(stmt).scalars().all()


    

