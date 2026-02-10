from uuid import UUID
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import enum
from app.core.database import Base


class MuscleRole(enum.Enum):
    primary = "primary"
    secondary = "secondary"


class ExerciseMuscle(Base):
    __tablename__ = "exercise_muscles"

    exercise_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("exercises.id"),
        primary_key=True
        )
    muscle_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("muscles.id"),
        primary_key=True
        )
    role: Mapped[MuscleRole] = mapped_column(
        Enum(MuscleRole),
        nullable=False
        )
    
    exercise = relationship("Exercise", back_populates="muscles")
    muscle = relationship("Muscle")
