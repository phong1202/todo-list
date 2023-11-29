"""Add user model and add relationship to ToDo model

Revision ID: 495ced4e6d3b
Revises: 
Create Date: 2023-11-22 17:47:57.542655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '495ced4e6d3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('to_do_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('to_do_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('users')
    # ### end Alembic commands ###