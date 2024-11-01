"""empty message

Revision ID: d7a730ce9b6c
Revises: cfd8e32957ec
Create Date: 2024-11-01 22:31:29.800021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a730ce9b6c'
down_revision = 'cfd8e32957ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.drop_constraint('votes_survey_id_fkey', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.create_foreign_key('votes_survey_id_fkey', 'surveys', ['survey_id'], ['id'])

    # ### end Alembic commands ###
