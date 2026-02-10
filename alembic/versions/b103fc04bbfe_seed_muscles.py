"""seed muscles

Revision ID: b103fc04bbfe
Revises: 418da07ae4a0
Create Date: 2026-02-10 13:24:07.834209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'b103fc04bbfe'
down_revision: Union[str, Sequence[str], None] = '418da07ae4a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


muscles = [
    ("Chest", "5667a02b-2bc8-4c29-ace3-e62aca240347"),
    ("Back", "75df3d4f-6942-4675-9692-5ea4d50c449c"),
    ("Shoulders", "151ea2d7-b8a6-420f-8b59-3c25d36c5a06"),
    ("Biceps", "7fbfa58e-2db6-4c39-8b89-7050cde20a9e"),
    ("Triceps", "eb8b2245-dd7b-412f-aea5-62edc154ac6d"),
    ("Quadriceps", "7b466e25-0ae1-49f2-8421-7ee44b4c040d"),
    ("Hamstrings", "27dce0d6-25e5-4ef8-954b-4caf66220752"),
    ("Glutes", "1306faa3-1c8b-490b-a964-342decdddc6a"),
    ("Calves", "3cfc1c1d-9bc9-49f5-9b2e-81c50fc36bd5"),
    ("Abdominals", "40b49ea7-adc9-455c-aa90-769c16cfad93"),
    ("Lower back", "80c5ae53-8325-4a8f-ac82-2a66617f0899"),
    ("Forearms", "a377f700-6d0f-4575-9d73-dbd7152b3aa0"),
    ("Trapezius", "7f5bf6e8-56ff-4853-819f-2e3e0c2537ef"),
    ("Lats", "d8f9c94c-85b7-41f0-b0d1-b84c9c0b2e27")
]


def upgrade() -> None:
    muscles_table = sa.table(
        "muscles",
        sa.column("id", sa.UUID()),
        sa.column("name", sa.String()),
    )

    op.bulk_insert(
        muscles_table,
        [{"id": uuid.UUID(id_str), "name": name} for name, id_str in muscles]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM muscles")
