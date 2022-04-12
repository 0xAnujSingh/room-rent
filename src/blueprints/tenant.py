
from flask import Blueprint, request
from sqlalchemy.orm import Session
from sqlalchemy import null, select, update

from datetime import datetime

from src.db import engine
from src.model import Tenant,Room

blueprint = Blueprint('tenant', 'tenant')

def convertDate(date_str):
    date_format = "%d/%m/%Y"

    return datetime.strptime(date_str, date_format).date()

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

            new_tenant = Tenant(
                name=name,
                aadhar_card=aadhar_card,
                balance=balance,
                mobile_number=mobile_number
            )
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
def updateTenantDetails(tenantId):
    try:
        with Session(engine) as session:
            data = request.json

            get_tenant_stmt = select(Tenant).where(Tenant.id == tenantId)
            tenant = session.scalar(get_tenant_stmt)

            if tenant is None:
                return { "error": "Tenant not found" }, 404

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

@blueprint.route('/tenant/<tenantId>/checkin', methods = ['POST'])
def roomCheckin(tenantId):
    ## Get room id, reading and start date from request body
    ## Get room from room_id from database
    ## Get tenant from tenantId from database
    ## Check if room does not already have a tenant
    ## Error out if given room reading is less than the current room reading

    try:
        with Session(engine) as session:
            data = request.json
            
            reading = data['room']['reading']
            roomId = data['room']['id']
            date_str = data['date']

            get_tenant_stmt = select(Tenant).where(Tenant.id == tenantId)
            tenant = session.scalar(get_tenant_stmt)

            if tenant is None:
                return { "error": "Tenant not found" }, 404

            get_room_stmt = select(Room).where(Room.id == roomId)
            room = session.scalar(get_room_stmt)

            ## Check if tenant if already checked in some other room
            if tenant.start_date is not None and tenant.leave_date is None:
                return { "error": "Tenant has already checked in" }

            if room is None:
                return { "error": "Room not found" }, 404
            elif reading < room.reading:
                return { "error": "Reading cannot be less then the exisiting reading" }

            if room.tenant_id is not None:
                return { "error": "Room is not available" }, 400
            
            # reading is not None and reading >= room.reading
            room.reading = reading
            room.tenant_id = tenant.id

            tenant.start_date = convertDate(date_str)

            if tenant.leave_date is not None:
                tenant.leave_date = None

            update(Tenant)
            update(Room)
            session.commit() 
        return { "success": True }
    except Exception as err:
        return { "success": False, "error": str(err) }

@blueprint.route('/tenant/<tenantId>/checkout', methods = ['POST'])
def roomCheckout(tenantId):            

    try:
        with Session(engine) as session:
            data = request.json
            
            ## Get Data from request
            roomId = data['room']['id']
            reading = data['room']['reading']
            date_str = data['date']
            leave_date = convertDate(date_str)

            ## Get data from database
            get_tenant_stmt = select(Tenant).where(Tenant.id == tenantId)
            tenant = session.scalar(get_tenant_stmt)

            get_room_stmt = select(Room).where(Room.id == roomId)
            room = session.scalar(get_room_stmt)

            ## Validate state change
            if tenant is None:
                return { "error": "Tenant not found" }, 404
            
            if tenant.start_date is None or (tenant.start_date is not None and tenant.leave_date is not None):
                return { "error": "Tenant is not in any room" }

            if tenant.start_date > leave_date:
                return { "error": "The leave date cannot be less than start date" }

            if room is None:
                return { "error": "Room not found"}, 404    
            elif reading < room.reading:
                return { "error": "Reading cannot be less then exisiting reading" }

            if room.tenant_id is None:
                return { "error": "Room is not used"}, 400


            ## Update state
            room.tenant_id = None
            room.reading = reading
            tenant.leave_date = leave_date

            update(Room)
            update(Tenant)
            session.commit()
        return { "success": True }
    except Exception as err:
        return { "success": False, "error": str(err) } 


