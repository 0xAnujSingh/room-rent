from os import getenv
from src.services.billing import chargeTenant

from sqlalchemy import update

ELECTRICITY_RATE = int(getenv('ELECTRICITY_RATE'))

def updateRoomReading(room, reading, session):
    units_consumed = (reading - room.reading)
    charges = units_consumed * ELECTRICITY_RATE
    room.reading = reading

    if room.tenant_id is not None:
        chargeTenant(room.tenant_id, charges, f"Electricity bill for {units_consumed} units", session)

    return