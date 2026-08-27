from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Loan

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.get("", summary="List loans")
def list_loans(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(Loan)
    total = q.count()
    items = q.offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{loan_id}", summary="Get loan")
def get_loan(loan_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(Loan).filter(Loan.loan_id == loan_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj
