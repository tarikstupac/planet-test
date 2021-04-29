"""Changed users table.

Revision ID: 115c193e8a26
Revises: b27422a7aa8e
Create Date: 2021-04-29 11:46:52.193882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '115c193e8a26'
down_revision = 'b27422a7aa8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_image', sa.String(length=150), nullable=True))
    op.drop_column('users', 'display_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('display_name', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.drop_column('users', 'profile_image')
    # ### end Alembic commands ###
