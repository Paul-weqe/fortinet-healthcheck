"""empty message

Revision ID: 30571e83357e
Revises: 9c60c12ee226
Create Date: 2022-07-26 08:03:49.775642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30571e83357e'
down_revision = '9c60c12ee226'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('devices_alias_key', 'devices', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('devices_alias_key', 'devices', ['alias'])
    # ### end Alembic commands ###