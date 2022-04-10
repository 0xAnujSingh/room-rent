
from flask import Blueprint, request, session
from sqlalchemy.orm import Session
from sqlalchemy import  delete, select, update

from datetime import datetime

from src.db import engine
from src.model import Tenant

blueprint = Blueprint('tenant', 'tenant')

def convertDate(date_str):
    date_format = "%d/%m/%Y"

    return datetime.strptime(date_str, date_format)

def toDict(tenant):
    return {
        "id": tenant.id,
        "name" : tenant.name,
        "aadhar_card": tenant.aadhar_card,
        "balance": tenant.balance,
        "mobile_number": tenant.mobile_number,
        "start_date": tenant.start_date,
        "leave_date": tenant.leave_date
    }

@blueprint.route('/tenant', methods = ['POST'])
def createTenantDetails():
    try:
        with Session(engine) as session:
            data = request.json 

            name = data['name']
            aadhar_card = data['aadhar_card']
            balance = data['balance']
            mobile_number = data['mobile_number']
            start_date = convertDate(data['start_date'])
            leave_date = convertDate(data['leave_date'])

            new_tenant = Tenant(name=name, aadhar_card=aadhar_card, balance=balance, mobile_number=mobile_number, start_date=start_date, leave_date=leave_date)
            session.add(new_tenant)
            session.commit()
    except Exception as err:
        return { "success" : False, "error" : str(err) }
    
    return { "success": True}

@blueprint.route('/tenant/<tenantId>', methods = ['GET'])
def getTenantDetails(tenantId):
    with Session(engine) as session:
        stmt = select(Tenant).where(Tenant.id== tenantId)
        tenant = session.scalar(stmt)

        if tenant is None:
            return { "error" : "Tenant not found" }, 404

        return toDict(tenant)

@blueprint.route('/tenant/<tenantId>', methods = ['PATCH'])
def updateRoomDetails(tenantId):
    try:
        with Session(engine) as session:
            data = request.json

            balance = data['balance']
            # leave_date = data['leave_date']

            get_tenant_stmt = select(Tenant).where(Tenant.id == tenantId)
            tenant = session.scalar(get_tenant_stmt)

            if tenant is None:
                return { "error": "Tenant not found" }, 404

            if balance is not None and balance >= 0:
                tenant.balance = balance

            # if leave_date is not None:
            #     pass

            update(Tenant)
            session.commit()
        return { "success": True }
    except Exception as err:
        return { "success": False, "error": str(err)}

@blueprint.route('/tenant/<tenantId>', methods = ['DELETE'])
def deleteTenantDetails(tenantId):
    try:
        with Session(engine) as session:
            get_tenant_stmt = select(Tenant).where(Tenant.id == tenantId)
            tenant = session.scalar(get_tenant_stmt)

            if tenant is None:
                return { "error" : "Room not found" }, 404
            
            session.delete(tenant)
            session.commit()
        return { "success": True }
    except Exception as err:
        return { "success": False, "error": str(err) }

@blueprint.route('/tenant', methods = ['GET'])
def listAllTenant():
    print("get rooms")
    with Session(engine) as session:
        tenants = [toDict(t) for t in session.query(Tenant).all()]
        
        return { "tenants": tenants }
