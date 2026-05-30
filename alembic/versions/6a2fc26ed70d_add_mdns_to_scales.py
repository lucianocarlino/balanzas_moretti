"""add mdns to scales

Revision ID: 6a2fc26ed70d
Revises: 359650b53273
Create Date: 2026-05-30 01:51:24.731400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a2fc26ed70d'
down_revision: Union[str, None] = '359650b53273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
