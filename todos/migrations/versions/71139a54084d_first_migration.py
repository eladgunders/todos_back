"""first_migration

Revision ID: 71139a54084d
Revises: 
Create Date: 2023-05-04 12:08:41.445166

"""
import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71139a54084d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('priority',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('category',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('created_by_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'created_by_id', name='unique_category')
    )
    op.create_table('todo',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('is_completed', sa.Boolean(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_by_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('priority_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['priority_id'], ['priority.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_category',
    sa.Column('todo_id', sa.BigInteger(), nullable=False),
    sa.Column('category_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('todo_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_category')
    op.drop_table('todo')
    op.drop_table('category')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('priority')
    # ### end Alembic commands ###
