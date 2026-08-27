from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import FraudSignal
from app.fraud.signals.engine import analyze_entity, persist_signals

router = APIRouter(prefix="/api/fraud", tags=["fraud"])

@router.get("/signals", summary="List fraud signals")
def list_signals(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    q = db.query(FraudSignal)
    total = q.count()
    items = q.order_by(FraudSignal.detected_at.desc()).offset((page-1)*size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/signals/{entity_type}/{entity_id}", summary="Signals for entity")
def signals_for(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    rows = db.query(FraudSignal).filter(FraudSignal.entity_type==entity_type, FraudSignal.entity_id==entity_id).all()
    return {"entity_type": entity_type, "entity_id": entity_id, "signals": rows, "count": len(rows)}

@router.post("/analyze/{entity_type}/{entity_id}", summary="Analyze entity for fraud signals")
def analyze(entity_type: str, entity_id: str, persist: bool = False, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    signals = analyze_entity(db, entity_type, entity_id)
    if persist and signals:
        persist_signals(db, entity_type, entity_id, signals)
    return {"entity_type": entity_type, "entity_id": entity_id, "signals": signals, "count": len(signals)}
