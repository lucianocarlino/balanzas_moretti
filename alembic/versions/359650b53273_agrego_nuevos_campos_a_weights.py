"""Agrego nuevos campos a weights

Revision ID: 359650b53273
Revises: e987e4d4932b
Create Date: 2026-05-13 10:55:51.325626

"""
from typing import Sequence, Union
from sqlalchemy import inspect
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '359650b53273'
down_revision: Union[str, None] = 'e987e4d4932b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('scales')]
    if 'mac' not in columns:
        op.add_column('scales', sa.Column('mac', sa.String(), nullable=True))
    if 'ip' not in columns:
        op.add_column('scales', sa.Column('ip', sa.String(), nullable=True))
    if 'nodemcu_status' not in columns:
        op.add_column('scales', sa.Column('nodemcu_status', sa.String(), nullable=True))
    if 'nodemcu_version' not in columns:
        op.add_column('scales', sa.Column('nodemcu_version', sa.String(), nullable=True))
    if 'comunicacion' not in columns:
        op.add_column('scales', sa.Column('comunicacion', sa.String(), nullable=True))


def downgrade() -> None:
    # Elimina las columnas agregadas si se revierte la migración
    op.drop_column('scales', 'comunicacion')
    op.drop_column('scales', 'nodemcu_version')
    op.drop_column('scales', 'nodemcu_status')
    op.drop_column('scales', 'ip')
    op.drop_column('scales', 'mac')
