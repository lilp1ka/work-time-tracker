"""удалил порно

Revision ID: 5a2eeb1a7e5d
Revises: e7bce430f2f6
Create Date: 2024-10-30 10:42:07.580375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a2eeb1a7e5d'
down_revision: Union[str, None] = 'e7bce430f2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'porno')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('porno', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
