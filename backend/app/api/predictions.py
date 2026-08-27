from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import Prediction
from app.ml.prediction.engine import predict, predict_and_store

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.get("/{entity_type}/{entity_id}", summary="Predictions for entity")
def list_preds(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    rows = db.query(Prediction).filter(Prediction.entity_type==entity_type, Prediction.entity_id==entity_id).order_by(Prediction.predicted_at.desc()).all()
    return {"entity_type": entity_type, "entity_id": entity_id, "predictions": rows, "count": len(rows)}

@router.post("/{entity_type}/{entity_id}", summary="Generate prediction")
def create_pred(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")
    obj = predict_and_store(db, entity_type, entity_id)
    return obj
