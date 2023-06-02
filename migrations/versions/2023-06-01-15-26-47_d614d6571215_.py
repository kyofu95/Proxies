"""empty message

Revision ID: d614d6571215
Revises: ff1e967acb17
Create Date: 2023-06-01 15:26:47.804338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd614d6571215'
down_revision = 'ff1e967acb17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health', schema=None) as batch_op:
        batch_op.alter_column('connections',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('failed_connections',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health', schema=None) as batch_op:
        batch_op.alter_column('failed_connections',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('connections',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
