from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.services.analysis_service import analyze_entity
from app.intelligence.risk.aggregator import collective_risk
from app.intelligence.risk.explanation import explain
from app.intelligence.anomaly.detector import anomaly_score_isolation
from app.intelligence.temporal.analyzer import growth_analysis, cluster_growth
from app.intelligence.features import build_all_features

router = APIRouter(prefix="/api/intelligence", tags=["intelligence"])

def _validate(entity_id: str):
    try: UUID(entity_id)
    except: raise HTTPException(400, "Invalid UUID")

@router.post("/analyze/{entity_type}/{entity_id}", summary="Full swarm analysis (rules+graph+anomaly+ML+temporal+risk+explain+alert)")
def analyze(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    return analyze_entity(db, entity_type, entity_id, persist=True)

@router.get("/features/{entity_type}/{entity_id}", summary="All features")
def feats(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    _validate(entity_id)
    return build_all_features(db, entity_type, entity_id)

@router.get("/risk/{entity_type}/{entity_id}", summary="Individual vs network vs collective risk")
def risk(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    _validate(entity_id)
    coll=collective_risk(db, entity_type, entity_id, persist=False)
    expl=explain(db, entity_type, entity_id, coll)
    return {"collective": coll, "explanation": expl}

@router.get("/anomaly/{entity_type}/{entity_id}", summary="Anomaly detection")
def anomaly(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    _validate(entity_id)
    return anomaly_score_isolation(db, entity_type, entity_id)

@router.get("/temporal/{entity_type}/{entity_id}", summary="Temporal intelligence")
def temporal(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    _validate(entity_id)
    return growth_analysis(db, entity_type, entity_id)

@router.get("/explain/{entity_type}/{entity_id}", summary="Explainable risk")
def explain_ep(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    _validate(entity_id)
    coll=collective_risk(db, entity_type, entity_id, persist=False)
    return explain(db, entity_type, entity_id, coll)
