"""Add itinerary column to trips

Revision ID: bb8c741a65ce
Revises: a80ccc48ac5b
Create Date: 2025-05-17 10:06:47.936991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8c741a65ce'
down_revision = 'a80ccc48ac5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.add_column(sa.Column('itinerary', sa.JSON(), nullable=True))
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))

    with op.batch_alter_table('trips', schema=None) as batch_op:
        batch_op.alter_column('updated_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
        batch_op.drop_column('itinerary')

    # ### end Alembic commands ###
