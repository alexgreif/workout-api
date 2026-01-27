"""seed muscles

Revision ID: 1fa3d4ac3bfe
Revises: 8dfa64d433d7
Create Date: 2026-01-27 11:41:15.316525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fa3d4ac3bfe'
down_revision: Union[str, Sequence[str], None] = '8dfa64d433d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


muscles = [
    "Chest",
    "Back",
    "Shoulders",
    "Biceps",
    "Triceps",
    "Quadriceps",
    "Hamstrings",
    "Glutes",
    "Calves",
    "Abdominals",
    "Lower back",
    "Forearms",
    "Trapezius",
    "Lats",
]


def upgrade() -> None:
    """Upgrade schema."""
    muscles_table = sa.table(
        "muscles",
        sa.column("name", sa.String())
    )

    op.bulk_insert(
        muscles_table,
        [{"name": muscle} for muscle in muscles]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM muscles")
