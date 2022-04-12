from sqlalchemy import select, update
from datetime import datetime

from src.model import Tenant, Transaction

def chargeTenant(tenant_id, amount, desc, session):
    get_tenant_stmt = select(Tenant).where(Tenant.id == tenant_id)
    tenant = session.scalar(get_tenant_stmt)

    transaction = Transaction(tenant_id=tenant_id, amount=amount, desc=desc, date=datetime.now())
    tenant.balance = tenant.balance + amount

    session.add(transaction)
