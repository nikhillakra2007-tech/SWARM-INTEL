from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Investigation, InvestigationAction
from app.schemas.schemas import InvestigationCreate
import uuid

router = APIRouter(prefix="/api/investigations", tags=["investigations"])

@router.get("", summary="List investigations")
def list_invs(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(Investigation)
    total = q.count()
    items = q.order_by(Investigation.opened_at.desc()).offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{investigation_id}", summary="Get investigation")
def get_inv(investigation_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(Investigation).filter(Investigation.investigation_id==investigation_id).first()
    if not obj: raise HTTPException(404, "Not found")
    actions = db.query(InvestigationAction).filter(InvestigationAction.investigation_id==investigation_id).order_by(InvestigationAction.performed_at).all()
    return {"investigation": obj, "actions": actions}

@router.post("", status_code=201, summary="Open investigation")
def create_inv(payload: InvestigationCreate, db: Session = Depends(get_db)):
    obj = Investigation(investigation_id=uuid.uuid4(), alert_id=payload.alert_id, investigator_ref=payload.investigator_ref, priority=payload.priority, notes=payload.notes)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
