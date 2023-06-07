"""add bs_color field for Color model

Revision ID: e63935157122
Revises: 72dab37cd6e7
Create Date: 2023-06-01 11:28:18.123350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e63935157122'
down_revision = '72dab37cd6e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Color', sa.Column('bs_name', sa.String(), nullable=True))
    op.alter_column('Color', 'code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Color', 'code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('Color', 'bs_name')
    # ### end Alembic commands ###