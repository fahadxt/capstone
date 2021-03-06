"""empty message

Revision ID: 4a2182c0e20c
Revises: ece5902c066d
Create Date: 2020-12-20 17:11:37.901472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a2182c0e20c'
down_revision = 'ece5902c066d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('actors', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actors', 'updated_at')
    op.drop_column('actors', 'created_at')
    # ### end Alembic commands ###
