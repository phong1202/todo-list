"""Fix bug password

Revision ID: 46697891630f
Revises: 567f5db7c48c
Create Date: 2023-11-26 13:30:58.787472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46697891630f'
down_revision = '567f5db7c48c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               nullable=True)

    # ### end Alembic commands ###
