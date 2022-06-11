"""0.4.0

Revision ID: 0e57f0ab2101
Revises: 5c889d53d173
Create Date: 2022-06-09 19:01:33.942306

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0e57f0ab2101'
down_revision = '5c889d53d173'
branch_labels = None
depends_on = None

event_type = sa.Enum('CREATE', 'UPDATE', 'COMMENT', name='eventtype')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('maintenance_comment', 'maintenance_event')
    op.rename_table('incident_comment', 'incident_event')

    event_type.create(op.get_bind())

    op.add_column('incident_event', sa.Column('type', event_type, nullable=False))
    op.add_column('maintenance_event', sa.Column('type', event_type, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('maintenance_event', 'type')
    op.drop_column('incident_event', 'type')

    event_type.drop(op.get_bind())

    op.rename_table('maintenance_event', 'maintenance_comment')
    op.rename_table('incident_event', 'incident_comment')
    # ### end Alembic commands ###
