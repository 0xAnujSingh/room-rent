from sqlalchemy import Column, String, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = True)
    number = Column(Integer, nullable =False)
    floor = Column(Integer, nullable = False)
    reading = Column(Integer, nullable =False)
    rent = Column(Integer, nullable = False)

class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(Integer, primary_key = True,autoincrement=True)
    name = Column(String(255), nullable = False)
    aadhar_card = Column(String(24), nullable = False)
    balance = Column(Integer, nullable = False)
    mobile_number = Column(String(16), nullable = False)
    start_date = Column(Date, nullable =True)
    last_rent_date = Column(Date, nullable =True)
    leave_date = Column(Date, nullable = True)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, autoincrement=True, primary_key = True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = True)
    bill_id = Column(Integer, ForeignKey('bill.id'), nullable = True)
    amount = Column(Integer, nullable = False)
    desc = Column(String(255), nullable = False)
    date = Column(Date, nullable = False)

class Bill(Base):
    __tablename__ = 'bill'
    id = Column(Integer, autoincrement = True,primary_key = True)
    label = Column(String(100))
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable = True)
    paid = Column(Integer, nullable = False)
