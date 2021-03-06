"""Create products table

Revision ID: 432d6fd1b1a5
Revises: 
Create Date: 2021-12-22 12:11:13.233576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '432d6fd1b1a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
