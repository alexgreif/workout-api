from pydantic import BaseModel, ConfigDict
from typing import List, Literal


class ExerciseMuscleCreate(BaseModel):
    muscle_id: int
    role: Literal["primary", "secondary"]


class ExerciseCreate(BaseModel):
    name: str
    description: str
    muscles: List[ExerciseMuscleCreate]


class ExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str