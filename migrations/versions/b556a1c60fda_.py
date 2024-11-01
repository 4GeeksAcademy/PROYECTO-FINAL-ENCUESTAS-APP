"""empty message

Revision ID: b556a1c60fda
Revises: d7a730ce9b6c
Create Date: 2024-11-01 22:34:21.131315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b556a1c60fda'
down_revision = 'd7a730ce9b6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.drop_column('survey_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('survey_id', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
