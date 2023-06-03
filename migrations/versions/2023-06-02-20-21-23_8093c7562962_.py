"""empty message

Revision ID: 8093c7562962
Revises: d614d6571215
Create Date: 2023-06-02 20:21:23.395768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8093c7562962'
down_revision = 'd614d6571215'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.create_unique_constraint("address_country_region_city_key", ['country', 'region', 'city'])

    with op.batch_alter_table('proxy', schema=None) as batch_op:
        batch_op.execute("CREATE TYPE proxyprotocol AS ENUM ('SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS')")
        batch_op.execute("ALTER TABLE proxy ALTER COLUMN protocol TYPE proxyprotocol USING protocol::text::proxyprotocol")
        batch_op.execute("DROP TYPE sqlproxyprotocol")
        # batch_op.alter_column('protocol',
        #        existing_type=postgresql.ENUM('UNKNOWN', 'SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS', name='sqlproxyprotocol'),
        #        type_=sa.Enum('SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS', name='proxyprotocol'),
        #        existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proxy', schema=None) as batch_op:
        batch_op.execute("CREATE TYPE sqlproxyprotocol AS ENUM ('UNKNOWN', 'SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS')")
        batch_op.execute("ALTER TABLE proxy ALTER COLUMN protocol TYPE sqlproxyprotocol USING protocol::text::sqlproxyprotocol")
        batch_op.execute("DROP TYPE proxyprotocol")
        # batch_op.alter_column('protocol',
        #        existing_type=sa.Enum('SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS', name='proxyprotocol'),
        #        type_=postgresql.ENUM('UNKNOWN', 'SOCKS4', 'SOCKS5', 'HTTP', 'HTTPS', name='sqlproxyprotocol'),
        #        existing_nullable=False)

    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_constraint("address_country_region_city_key", type_='unique')

    # ### end Alembic commands ###