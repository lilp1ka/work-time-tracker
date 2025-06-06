"""Fix team-member relationship

Revision ID: a899a38cb1fd
Revises: 70feebae6d97
Create Date: 2024-12-30 13:16:56.215433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a899a38cb1fd'
down_revision: Union[str, None] = '70feebae6d97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('team_members_team_id_user_id_key', 'team_members', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('team_members_team_id_user_id_key', 'team_members', ['team_id', 'user_id'])
    # ### end Alembic commands ###
