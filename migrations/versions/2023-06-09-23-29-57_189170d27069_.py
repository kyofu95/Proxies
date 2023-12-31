"""empty message

Revision ID: 189170d27069
Revises: 8093c7562962
Create Date: 2023-06-09 23:29:57.065617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '189170d27069'
down_revision = '8093c7562962'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proxy', schema=None) as batch_op:
        batch_op.drop_column('anonymity_level')
        batch_op.drop_column('login')
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proxy', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('login', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('anonymity_level', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
