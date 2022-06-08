"""0.1.0

Revision ID: 128dc0fc058c
Revises: 96401e5e2911
Create Date: 2022-06-06 15:37:20.020451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '128dc0fc058c'
down_revision = '96401e5e2911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scope',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('UP', 'DEGRADED', 'DOWN', name='servicestatus'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('incident',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('external_reference', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'STABLE', 'RESOLVED', 'COMPLETED', name='incidentstatus'), nullable=False),
    sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MODERATE', 'LOW', 'MINOR', name='incidentseverity'), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('start_impact_date', sa.DateTime(), nullable=True),
    sa.Column('resolve_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['scope_id'], ['scope.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maintenance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('external_reference', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('CREATED', 'VALIDATED', 'SHEDULED', 'IN_PROGRESS', 'SUCCESS', 'FAILED', name='maintenancestatus'), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('service_planned_status', sa.Enum('UP', 'DEGRADED', 'DOWN', name='servicestatus'), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('scheduled_start_date', sa.DateTime(), nullable=False),
    sa.Column('scheduled_end_date', sa.DateTime(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['scope_id'], ['scope.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('incident_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('incident_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['incident_id'], ['incident.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maintenance_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('maintenance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['maintenance_id'], ['maintenance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('maintenance_comment')
    op.drop_table('incident_comment')
    op.drop_table('maintenance')
    op.drop_table('incident')
    op.drop_table('service')
    op.drop_table('scope')
    # ### end Alembic commands ###
