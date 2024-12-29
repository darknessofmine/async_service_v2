"""created profiles table

Revision ID: aad5b21bea4a
Revises: d4829bafcd23
Create Date: 2024-12-29 21:18:44.073043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'aad5b21bea4a'
down_revision: Union[str, None] = 'd4829bafcd23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'profiles',
        sa.Column('fist_name', sa.String(length=32), nullable=False),
        sa.Column('last_name', sa.String(length=32), nullable=True),
        sa.Column('bio', sa.String(length=500), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq__profile__user_id')
    )


def downgrade() -> None:
    op.drop_table('profiles')
