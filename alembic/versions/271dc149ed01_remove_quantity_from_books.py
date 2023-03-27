"""remove quantity from books

Revision ID: 271dc149ed01
Revises: 4e16db873168
Create Date: 2023-03-26 21:21:57.341502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '271dc149ed01'
down_revision = '4e16db873168'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
