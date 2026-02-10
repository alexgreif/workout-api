from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.exercise import Exercise
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
            exercise_id: UUID,
            muscle_id: UUID,
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
            exercise_id: UUID,
            muscles: list[tuple[UUID, str]]
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


    def list_by_user_id(self, user_id: UUID) -> list[Exercise]:
        stmt = (
            select(Exercise)
            .options(
                    selectinload(Exercise.muscles)
                    .selectinload(ExerciseMuscle.muscle)
                )
            .where(
                Exercise.created_by_user_id == user_id
            )
        )
        return list(self.db.scalars(stmt))
    

    def get_by_id_and_user_id(
            self,
            *,
            exercise_id: UUID,
            user_id: UUID
    ) -> Exercise | None:
        stmt = (
            select(Exercise)
            .options(
                    selectinload(Exercise.muscles)
                    .selectinload(ExerciseMuscle.muscle)
                )
            .where(
                Exercise.id == exercise_id,
                Exercise.created_by_user_id == user_id
            )
        )
        return self.db.scalar(stmt)
