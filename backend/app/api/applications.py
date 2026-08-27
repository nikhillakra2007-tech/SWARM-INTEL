from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import LoanApplication
from app.schemas.schemas import ApplicationCreate

router = APIRouter(prefix="/api/applications", tags=["applications"])

@router.get("", summary="List applications")
def list_apps(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(LoanApplication)
    total = q.count()
    items = q.order_by(LoanApplication.application_timestamp.desc()).offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{application_id}", summary="Get application")
def get_app(application_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(LoanApplication).filter(LoanApplication.application_id == application_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.post("", status_code=201, summary="Create application")
def create_app(payload: ApplicationCreate, db: Session = Depends(get_db)):
    import uuid
    if db.query(LoanApplication).filter(LoanApplication.application_ref == payload.application_ref).first():
        raise HTTPException(400, "application_ref exists")
    obj = LoanApplication(application_id=uuid.uuid4(), **payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
