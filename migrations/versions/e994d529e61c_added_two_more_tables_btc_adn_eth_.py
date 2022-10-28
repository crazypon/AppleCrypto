"""added two more tables BTC adn ETH payments and removed Purchases table

Revision ID: e994d529e61c
Revises: 5de8b871a180
Create Date: 2022-10-25 17:19:18.038234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e994d529e61c'
down_revision = '5de8b871a180'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('btc_payments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('transaction_hash', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customers.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_hash')
    )
    op.create_table('eth_payments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('transaction_key', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customers.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_key')
    )
    op.drop_table('purchases')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchases',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('transaction_hash', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=5), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customers.user_id'], name='purchases_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='purchases_pkey'),
    sa.UniqueConstraint('transaction_hash', name='purchases_transaction_hash_key')
    )
    op.drop_table('eth_payments')
    op.drop_table('btc_payments')
    # ### end Alembic commands ###