from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("", summary="List customers")
def list_customers(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(Customer)
    total = q.count()
    items = q.offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{customer_id}", summary="Get customer")
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not obj: raise HTTPException(404, "Customer not found")
    return obj

@router.post("", status_code=201, summary="Create customer")
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    import uuid
    if db.query(Customer).filter(Customer.customer_ref == payload.customer_ref).first():
        raise HTTPException(400, "customer_ref already exists")
    obj = Customer(customer_id=uuid.uuid4(), **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/{customer_id}", summary="Update customer")
def update_customer(customer_id: UUID, payload: CustomerUpdate, db: Session = Depends(get_db)):
    obj = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not obj: raise HTTPException(404, "Customer not found")
    for k,v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj
