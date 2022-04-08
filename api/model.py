from os import getenv

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from api import app

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True,autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = False)
    number = Column(Integer, nullable =False)
    floor = Column(Integer, nullable = False)
    reading = Column(Integer, nullable =False)
    rent = Column(Integer, nullable = False)

class Tenant(db.Model):
    __tablename__ = 'tenant'
    id = Column(Integer, primary_key = True,autoincrement=True)
    name = Column(String(255), nullable = False)
    aadhar_card = Column(String(24), nullable = False)
    balance = Column(Integer, nullable = False)
    mobile_number = Column(String(16), nullable = False)
    start_date = Column(Date, nullable =True)
    leave_date = Column(Date, nullable = True)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = Column(Integer, autoincrement=True, primary_key = True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = True)
    bill_id = Column(Integer, ForeignKey('bill.id'),nullable = False)
    amount = Column(Integer, nullable = False)
    desc = Column(String(255), nullable = False)
    date = Column(Date, nullable = False)

class Bill(db.Model):
    __tablename__ = 'bill'
    id = Column(Integer, autoincrement = True,primary_key = True)
    label = Column(String(100))
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = False)
    paid = Column(Integer, nullable = False)
