"""0.2.0

Revision ID: 647227471a57
Revises: 128dc0fc058c
Create Date: 2022-06-07 21:11:59.686252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647227471a57'
down_revision = '128dc0fc058c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('version', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('version')
    )
    # ### end Alembic commands ###
