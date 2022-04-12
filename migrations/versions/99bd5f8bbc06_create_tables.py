"""Create tables

Revision ID: 99bd5f8bbc06
Revises: 
Create Date: 2022-04-12 21:51:16.696222

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '99bd5f8bbc06'
down_revision = None
branch_labels = None
depends_on = None

from src.model import Base
from src.db import engine

def upgrade():
    Base.metadata.create_all(engine)

def downgrade():
    Base.metadata.drop_all(engine)
