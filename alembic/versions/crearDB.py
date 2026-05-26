"""
Migración especial: crearDB
Crea todas las tablas y relaciones según los modelos actuales.
No depende de migraciones previas.
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Tabla packages
    op.create_table(
        'packages',
        sa.Column('package_id', sa.Integer, primary_key=True),
        sa.Column('expected_weight', sa.Float),
        sa.Column('minimum_weight', sa.Float),
        sa.Column('maximum_weight', sa.Float),
        sa.Column('name', sa.String, unique=True),
        sa.Column('active', sa.Boolean, default=True)
    )

    # Tabla scales
    op.create_table(
        'scales',
        sa.Column('scale_id', sa.Integer, primary_key=True),
        sa.Column('slave_address', sa.Integer, index=True, nullable=True, default=-1),
        sa.Column('name', sa.String, unique=True),
        sa.Column('online', sa.Boolean, default=False),
        sa.Column('mapped', sa.Boolean, default=False),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('mac', sa.String, nullable=True),
        sa.Column('ip', sa.String, nullable=True),
        sa.Column('nodemcu_status', sa.String, nullable=True),
        sa.Column('nodemcu_version', sa.String, nullable=True),
        sa.Column('comunicacion', sa.String, nullable=True)
    )

    # Tabla scales_has_packages
    op.create_table(
        'scales_has_packages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('scale_id', sa.Integer, sa.ForeignKey('scales.scale_id')),
        sa.Column('package_id', sa.Integer, sa.ForeignKey('packages.package_id'))
    )

    # Tabla weights
    op.create_table(
        'weights',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('date_time', sa.DateTime),
        sa.Column('initial_weight', sa.Float),
        sa.Column('final_weight', sa.Float),
        sa.Column('scale_id', sa.Integer, sa.ForeignKey('scales.scale_id')),
        sa.Column('package_id', sa.Integer, sa.ForeignKey('packages.package_id'))
    )

def downgrade():
    op.drop_table('weights')
    op.drop_table('scales_has_packages')
    op.drop_table('scales')
    op.drop_table('packages')

