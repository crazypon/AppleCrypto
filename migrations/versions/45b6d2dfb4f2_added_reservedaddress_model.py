"""added ReservedAddress model

Revision ID: 45b6d2dfb4f2
Revises: 9a73d745c879
Create Date: 2022-10-30 20:04:54.523890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45b6d2dfb4f2'
down_revision = '9a73d745c879'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserved_addresses',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('eth_address', sa.String(), nullable=True),
    sa.Column('reserved_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reserved_addresses')
    # ### end Alembic commands ###
