"""Initial tables setup

Revision ID: de9ee2e6cdb6
Revises: 
Create Date: 2024-08-21 15:33:12.915898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de9ee2e6cdb6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaigns_id'), 'campaigns', ['id'], unique=False)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_campaigns_id'), table_name='campaigns')
    op.drop_table('campaigns')
    # ### end Alembic commands ###
