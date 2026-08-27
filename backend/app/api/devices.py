from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Device, CustomerDeviceLink, Customer

router = APIRouter(prefix="/api/devices", tags=["devices"])

@router.get("/{device_id}", summary="Get device")
def get_device(device_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(Device).filter(Device.device_id == device_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.get("/{device_id}/customers", summary="Customers sharing device")
def device_customers(device_id: UUID, db: Session = Depends(get_db)):
    if not db.query(Device).filter(Device.device_id == device_id).first():
        raise HTTPException(404, "Device not found")
    links = db.query(CustomerDeviceLink).filter(CustomerDeviceLink.device_id == device_id).all()
    cids = [l.customer_id for l in links]
    customers = db.query(Customer).filter(Customer.customer_id.in_(cids)).all() if cids else []
    return {"device_id": device_id, "customers": customers, "count": len(customers)}
