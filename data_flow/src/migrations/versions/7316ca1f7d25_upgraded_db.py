"""upgraded db

Revision ID: 7316ca1f7d25
Revises: 54d1ee5d08f3
Create Date: 2024-11-08 13:28:03.599503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7316ca1f7d25'
down_revision: Union[str, None] = '54d1ee5d08f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_currencies_id', table_name='currencies')
    op.create_unique_constraint(None, 'currencies', ['name'])
    op.create_unique_constraint(None, 'currencies', ['id'])
    op.add_column('currency_data', sa.Column('source', sa.String(), nullable=True))
    op.add_column('currency_data', sa.Column('trust_factor', sa.Float(), nullable=True))
    op.add_column('currency_data_history', sa.Column('source', sa.String(), nullable=True))
    op.add_column('currency_data_history', sa.Column('trust_factor', sa.Float(), nullable=True))
    op.add_column('currency_data_history', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_unique_constraint(None, 'currency_data_history', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'currency_data_history', type_='unique')
    op.drop_column('currency_data_history', 'created_at')
    op.drop_column('currency_data_history', 'trust_factor')
    op.drop_column('currency_data_history', 'source')
    op.drop_column('currency_data', 'trust_factor')
    op.drop_column('currency_data', 'source')
    op.drop_constraint(None, 'currencies', type_='unique')
    op.drop_constraint(None, 'currencies', type_='unique')
    op.create_index('ix_currencies_id', 'currencies', ['id'], unique=True)
    # ### end Alembic commands ###