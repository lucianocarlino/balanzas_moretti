"""add mdns to scales

Revision ID: add_mdns_001
Revises: e987e4d4932b
Create Date: 2026-06-01

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_mdns_001'
down_revision = '359650b53273'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('scales', sa.Column('mdns', sa.String(), nullable=True))

def downgrade():
    op.drop_column('scales', 'mdns')