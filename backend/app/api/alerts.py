from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import FraudAlert

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("", summary="List alerts")
def list_alerts(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100), status: str | None = None):
    q = db.query(FraudAlert)
    if status: q = q.filter(FraudAlert.alert_status==status)
    total = q.count()
    items = q.order_by(FraudAlert.generated_at.desc()).offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{alert_id}", summary="Get alert")
def get_alert(alert_id: UUID, db: Session = Depends(get_db)):
    obj = db.query(FraudAlert).filter(FraudAlert.alert_id==alert_id).first()
    if not obj: raise HTTPException(404, "Not found")
    return obj
