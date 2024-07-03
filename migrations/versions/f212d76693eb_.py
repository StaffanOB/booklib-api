"""empty message

Revision ID: f212d76693eb
Revises: bbf54f4f4ce0
Create Date: 2024-07-03 13:53:33.379667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f212d76693eb'
down_revision = 'bbf54f4f4ce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.drop_constraint('authors_book_id_fkey', type_='foreignkey')
        batch_op.drop_column('book_id')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('authors_book_id_fkey', 'books', ['book_id'], ['id'])

    # ### end Alembic commands ###
