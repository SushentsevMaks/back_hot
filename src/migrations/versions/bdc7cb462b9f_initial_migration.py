"""initial migration

Revision ID: bdc7cb462b9f
Revises: 
Create Date: 2025-01-29 10:44:25.416030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdc7cb462b9f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('location', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('hotels')

