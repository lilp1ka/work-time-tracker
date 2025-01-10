"""Удаление колонки type_subscribe

Revision ID: 70feebae6d97
Revises: 5a2eeb1a7e5d
Create Date: 2024-12-30 12:46:29.672293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70feebae6d97'
down_revision: Union[str, None] = '5a2eeb1a7e5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('teams', 'type_subscribe')


def downgrade() -> None:
    op.add_column('teams', sa.Column('type_subscribe', sa.String(length=255), nullable=True))
