from sqlalchemy.orm import Session

from app.repositories.exercise import (
    ExerciseRepository,
    ExerciseNotFoundError
    )
from app.models.exercise import Exercise


class ExerciseService:
    def __init__(self, db: Session, exercise_repo: ExerciseRepository):
        self.db = db
        self.exercise_repo = exercise_repo

    def add_exercise(
            self,
            *,
            name: str,
            description: str | None,
            created_by_user_id: int,
            muscles: list[tuple[int, str]]
    ) -> Exercise:
        exercise = Exercise(
            name=name,
            description=description,
            created_by_user_id=created_by_user_id
        )

        self.exercise_repo.create(exercise)

        for muscle_id, role in muscles:
            self.exercise_repo.add_muscle(
                exercise_id=exercise.id,
                muscle_id=muscle_id,
                role=role
            )

        self.db.commit()
        return exercise
    
    
    def get_exercise(self, *, exercise_id: int) -> Exercise | None:
        return self.exercise_repo.get_by_id(exercise_id=exercise_id)
    
    
    def list_exercises(self) -> list[Exercise]:
        return self.exercise_repo.list_all()
    