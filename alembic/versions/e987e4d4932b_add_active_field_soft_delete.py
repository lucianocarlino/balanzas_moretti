"""add_active_field_soft_delete

Revision ID: e987e4d4932b
Revises: ebfd958cbc4b
Create Date: 2026-01-19 12:11:29.071039

"""
from typing import Sequence, Union
from sqlalchemy import inspect
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e987e4d4932b'
down_revision: Union[str, None] = 'ebfd958cbc4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('scales')]
    if 'active' not in columns:
        op.add_column('scales', sa.Column('active', sa.Boolean(), nullable=True, server_default='true'))


def downgrade() -> None:
    # Eliminar campo active de scales
    op.drop_column('scales', 'active')
    # Eliminar campo active de packages
    op.drop_column('packages', 'active')
