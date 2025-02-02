"""Initial migration

Revision ID: 240ab3d23f77
Revises: 
Create Date: 2024-11-08 12:55:08.429723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '240ab3d23f77'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('market_cap', sa.Float(), nullable=True),
    sa.Column('price_history', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('market_cap_history', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_id'), 'currencies', ['id'], unique=False)
    op.create_index(op.f('ix_currencies_name'), 'currencies', ['name'], unique=False)
    op.create_table('currencies_history',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('market_cap', sa.Float(), nullable=True),
    sa.Column('price_history', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('market_cap_history', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_history_id'), 'currencies_history', ['id'], unique=False)
    op.create_index(op.f('ix_currencies_history_name'), 'currencies_history', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_currencies_history_name'), table_name='currencies_history')
    op.drop_index(op.f('ix_currencies_history_id'), table_name='currencies_history')
    op.drop_table('currencies_history')
    op.drop_index(op.f('ix_currencies_name'), table_name='currencies')
    op.drop_index(op.f('ix_currencies_id'), table_name='currencies')
    op.drop_table('currencies')
    # ### end Alembic commands ###
