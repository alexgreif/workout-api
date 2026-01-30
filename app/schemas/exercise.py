from pydantic import BaseModel, ConfigDict
from typing import List

from app.models.exercise_muscle import MuscleRole


class ExerciseMuscleCreate(BaseModel):
    muscle_id: int
    role: MuscleRole


class ExerciseCreate(BaseModel):
    name: str
    description: str | None = None
    muscles: List[ExerciseMuscleCreate]


class MuscleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ExerciseMuscleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    muscle: MuscleRead
    role: MuscleRole


class ExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    muscles: List[ExerciseMuscleRead]
