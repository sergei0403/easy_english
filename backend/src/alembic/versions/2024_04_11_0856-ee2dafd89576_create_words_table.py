"""create words_table

Revision ID: ee2dafd89576
Revises: 61d99415d703
Create Date: 2024-04-11 08:56:56.210547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee2dafd89576'
down_revision: Union[str, None] = '61d99415d703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('words_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('english_phrase', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('translations_list', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_words_table_id'), 'words_table', ['id'], unique=False)
    op.create_index(op.f('ix_words_table_slug'), 'words_table', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_words_table_slug'), table_name='words_table')
    op.drop_index(op.f('ix_words_table_id'), table_name='words_table')
    op.drop_table('words_table')
    # ### end Alembic commands ###