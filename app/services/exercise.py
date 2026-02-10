from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repositories.exercise import ExerciseRepository
from app.models.exercise import Exercise
from app.models.user import User
from app.models.muscle import Muscle
from app.domain.errors import InvalidMuscleError, ExerciseNotFoundError


class ExerciseService:
    def __init__(self, db: Session, exercise_repo: ExerciseRepository):
        self.db = db
        self.exercise_repo = exercise_repo

    def add_exercise(
            self,
            *,
            name: str,
            description: str | None,
            created_by_user_id: UUID,
            muscles: list[tuple[UUID, str]]
    ) -> Exercise:
        exercise = Exercise(
            name=name,
            description=description,
            created_by_user_id=created_by_user_id
        )

        # Check if all muscles exist
        muscle_ids = {muscle_id for muscle_id, _ in muscles}
        stmt = select(Muscle.id).where(Muscle.id.in_(muscle_ids))
        existing_ids = set(self.db.execute(stmt).scalars().all())
        missing_ids = muscle_ids - existing_ids
        if missing_ids:
            raise InvalidMuscleError(missing_ids)

        self.exercise_repo.create(exercise)
        self.exercise_repo.add_muscles(exercise.id, muscles)
        self.db.commit()

        return exercise
    
    
    def get_exercise(self, *, exercise_id: UUID, user: User) -> Exercise:
        exercise = self.exercise_repo.get_by_id_and_user_id(
            exercise_id=exercise_id,
            user_id=user.id
        )

        if exercise is None:
            raise ExerciseNotFoundError()
        
        return exercise
    
    
    def list_exercises(self, *, user: User) -> list[Exercise]:
        return self.exercise_repo.list_by_user_id(user.id)
    