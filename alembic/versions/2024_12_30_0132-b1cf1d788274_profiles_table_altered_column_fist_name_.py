"""profiles table: altered column fist_name -> first_name

Revision ID: b1cf1d788274
Revises: 964a1a06b5e6
Create Date: 2024-12-30 01:32:53.614411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b1cf1d788274'
down_revision: Union[str, None] = '964a1a06b5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'profiles',
        sa.Column(
            'first_name',
            sa.String(length=32),
            nullable=False,
        ),
    )
    op.drop_column('profiles', 'fist_name')


def downgrade() -> None:
    op.add_column(
        'profiles',
        sa.Column(
            'fist_name',
            sa.VARCHAR(length=32),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column('profiles', 'first_name')
