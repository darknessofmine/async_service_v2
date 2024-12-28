"""users: added is_verified column

Revision ID: d4829bafcd23
Revises: 86703e08bca1
Create Date: 2024-12-28 20:06:42.356970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4829bafcd23'
down_revision: Union[str, None] = '86703e08bca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
