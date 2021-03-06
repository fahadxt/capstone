"""empty message

Revision ID: ece5902c066d
Revises: 295d3dc70d54
Create Date: 2020-12-17 20:38:53.644507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece5902c066d'
down_revision = '295d3dc70d54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('movies', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'updated_at')
    op.drop_column('movies', 'created_at')
    # ### end Alembic commands ###
