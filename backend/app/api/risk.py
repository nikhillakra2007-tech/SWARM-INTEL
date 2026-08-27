from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import RiskScore
from app.fraud.scoring.engine import calculate_risk

router = APIRouter(prefix="/api/risk", tags=["risk"])

@router.get("/{entity_type}/{entity_id}", summary="Latest risk + history")
def get_risk(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    rows = db.query(RiskScore).filter(RiskScore.entity_type==entity_type, RiskScore.entity_id==entity_id).order_by(RiskScore.calculated_at.desc()).all()
    if not rows: raise HTTPException(404, "No risk scores found")
    return {"entity_type": entity_type, "entity_id": entity_id, "latest": rows[0], "history": rows, "count": len(rows)}

@router.post("/{entity_type}/{entity_id}", summary="Recalculate risk")
def recalc(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    obj, signals = calculate_risk(db, entity_type, entity_id)
    return {"risk": obj, "signals": signals}
