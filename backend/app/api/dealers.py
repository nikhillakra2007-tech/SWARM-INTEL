from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Dealer, DealerCustomerLink

router = APIRouter(prefix="/api/dealers", tags=["dealers"])

@router.get("", summary="List dealers")
def list_dealers(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(Dealer)
    total = q.count()
    return {"items": q.offset((page-1)*size).limit(size).all(), "total": total, "page": page, "size": size}

@router.get("/{dealer_id}", summary="Get dealer")
def get_dealer(dealer_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(Dealer).filter(Dealer.dealer_id == dealer_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj
