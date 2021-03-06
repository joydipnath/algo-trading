"""added avatar column in users table

Revision ID: defbe41e837c
Revises: 
Create Date: 2021-04-05 13:52:52.696597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'defbe41e837c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'avatar')
    # ### end Alembic commands ###
