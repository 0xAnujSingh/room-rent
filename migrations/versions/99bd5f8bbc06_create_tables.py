"""Create tables

Revision ID: 99bd5f8bbc06
Revises: 
Create Date: 2022-04-12 21:51:16.696222

"""
from alembic import op
from sqlalchemy import Column, String, Integer, Date, ForeignKey

# revision identifiers, used by Alembic.
revision = '99bd5f8bbc06'
down_revision = None
branch_labels = None
depends_on = None

from src.model import Room, Tenant, Transaction, Bill

def upgrade():
    op.create_table(
        Tenant.__tablename__,
        Column('id', Integer, primary_key = True,autoincrement=True),
        Column('name', String(255), nullable = False),
        Column('aadhar_card', String(24), nullable = False),
        Column('balance', Integer, nullable = False),
        Column('mobile_number', String(16), nullable = False),
        Column('start_date', Date, nullable =True),
        Column('last_rent_date', Date, nullable =True),
        Column('leave_date', Date, nullable = True),
    )

    op.create_table(
        Room.__tablename__,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('tenant_id', Integer, ForeignKey('tenant.id'), nullable = True),
        Column('number', Integer, nullable =False),
        Column('floor', Integer, nullable = False),
        Column('reading', Integer, nullable =False),
        Column('rent', Integer, nullable = False)
    )

    op.create_table(
        Bill.__tablename__,
        Column('id', Integer, autoincrement = True,primary_key = True),
        Column('label', String(100)),
        Column('tenant_id', Integer, ForeignKey('tenant.id'), nullable = True),
        Column('paid', Integer, nullable = False),
    )

    op.create_table(
        Transaction.__tablename__,
        Column('id', Integer, autoincrement=True, primary_key = True),
        Column('tenant_id', Integer, ForeignKey('tenant.id'), nullable = True),
        Column('bill_id', Integer, ForeignKey('bill.id'), nullable = True),
        Column('amount', Integer, nullable = False),
        Column('desc', String(255), nullable = False),
        Column('date', Date, nullable = False)
    )

def downgrade():
    op.drop_table(Transaction.__tablename__)
    op.drop_table(Bill.__tablename__)
    op.drop_table(Room.__tablename__)
    op.drop_table(Tenant.__tablename__)
