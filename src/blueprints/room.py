from flask import Blueprint, request
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from src.db import engine
from src.model import Room

blueprint = Blueprint('room', 'room')

def toDict(room):
    return {"id" : room.id,
            "floor" : room.floor,
            "number" : room. number,
            "rent" : room.rent,
            "reading": room.reading,
            "tenant": room.tenant_id
        }

@blueprint.route('/room', methods = ['POST'])
def createRoomDetails():
    try:
        with Session(engine) as session:
            data = request.json

            floor = data['floor']
            reading = data['reading']
            number = data['number']
            rent = data['rent']

            new_room = Room(rent=rent, floor=floor, number = number, reading = reading)

            session.add(new_room)
            session.commit()
    except Exception as err:
        return { "success": False, "error": str(err) }

    return { "success": True }

@blueprint.route('/room/<roomId>', methods = ['GET'])
def getRoomDetails(roomId):
    with Session(engine) as session:
        stmt = select(Room).where(Room.id == roomId)

        room = session.scalar(stmt)

        if room is None:
            return { "error": "Room not found" }, 404

        return { "id": room.id,
                "floor": room.floor,
                "number": room.number,
                "rent": room.rent,
                "reading": room.reading,
                "tenant": room.tenant_id
            }

@blueprint.route('/room/<roomId>', methods = ['PATCH'])
def updateRoomDetails(roomId):
    try:
        with Session(engine) as session:
            data = request.json

            reading = data['reading']
            rent = data['rent']

            get_room_stmt = select(Room).where(Room.id == roomId)
            room = session.scalar(get_room_stmt)

            if room is None:
                return { "error": "Room Not Found" }, 404

            ## If reading is updated, then it must be greater than the existing reading.
            ## i.e reading cannot be reduced
            if reading is not None and reading > room.reading:
                room.reading = reading

            ## If rent is updated, it can never be zero
            if rent is not None and rent > 0:
                room.rent = rent

            update()

            session.commit()
        return { "success": True }
    except Exception as err:
        return { "success": False, "error" : str(err) }

@blueprint.route('/room/<roomId>', methods = ['DELETE'])
def deleteRoomDetails(roomId):
    try:
        with Session(engine) as session:
            get_room_stmt = select(Room).where(Room.id == roomId)
            room = session.scalar(get_room_stmt)

            if room is None:
                return { "error" : "Room not found" }, 404
            
            session.delete(room)
            session.commit()
        return { "success": True }
    except Exception as err:
        return { "success": False, "error": str(err) }
    
@blueprint.route('/room', methods = ['GET'])
def listAllRooms():
    with Session(engine) as session:
        room = [toDict(r) for r in session.query(Room).all()] 
        return { "room": room}

