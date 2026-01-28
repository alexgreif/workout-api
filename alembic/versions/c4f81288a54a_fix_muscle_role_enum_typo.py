"""fix muscle role enum typo

Revision ID: c4f81288a54a
Revises: 1fa3d4ac3bfe
Create Date: 2026-01-28 10:41:34.700888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4f81288a54a'
down_revision: Union[str, Sequence[str], None] = '1fa3d4ac3bfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE musclerole RENAME VALUE 'scondary' TO 'secondary'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE musclerole RENAME VALUE 'secondary' TO 'scondary'")
