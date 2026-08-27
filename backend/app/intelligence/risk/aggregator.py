from sqlalchemy.orm import Session
import uuid, sys, pathlib
from datetime import datetime, timezone
from .scorer import individual_risk, network_risk, risk_level
from app.models import RiskScore
from app.config import get_settings
settings=get_settings()
# Unified feature contract: model/inference is source of truth for ML
sys.path.insert(0, str(pathlib.Path(__file__).parents[4]))
try:
    from model.inference.predict import predict_from_db as model_predict
    def _ml_predict(db, et, eid):
        r = model_predict(db, et, eid)
        return {"probability": r["fraud_probability"], "label": r["prediction"], "model_version": r["model_version"]}
except Exception:
    from app.intelligence.ml.prediction import predict as _ml_predict

def collective_risk(db: Session, entity_type: str, entity_id: str, persist: bool=True) -> dict:
    """
    Swarm Risk Engine - documented composition to prevent double counting:
    - individual_risk: non-network rules only (e.g., REPLACEMENT, BURST without shared)
    - network_risk: shared-entity rules + degree/density/high-risk neighbors ONLY (no ML, no anomaly)
    - ml: model/inference fraud_probability (0-1) → scaled 0-100
    Weights: 0.25*individual + 0.45*network + 0.30*ML = collective 0-100.
    Anomaly is informational (affects confidence, not direct score) to avoid double count.
    """
    indiv=individual_risk(db, entity_type, entity_id)
    net=network_risk(db, entity_type, entity_id)
    ml=_ml_predict(db, entity_type, entity_id)
    w_ind=0.25; w_net=0.45; w_ml=0.30
    collective = round(indiv["score"]*w_ind + net["score"]*w_net + ml["probability"]*100*w_ml,2)
    collective=min(100, collective)
    level=risk_level(collective)
    # confidence uses anomaly separately (not score double count)
    try:
        from app.intelligence.anomaly.detector import anomaly_score_isolation
        anom=anomaly_score_isolation(db, entity_type, entity_id)
        anom_score=anom["anomaly_score"]
    except: anom_score=0.3
    confidence= round((anom_score*0.3 + ml["probability"]*0.4 + min(1, net["degree"]/5)*0.3),2) if net["degree"] else round((anom_score*0.2 + ml["probability"]*0.5),2)
    result={
        "individual_risk_score": indiv["score"],
        "individual_level": indiv["level"],
        "network_risk_score": net["score"],
        "network_level": net["level"],
        "fraud_probability": round(float(ml["probability"]),4),
        "model_version": ml.get("model_version", settings.MODEL_VERSION),
        "collective_risk_score": collective,
        "risk_level": level,
        "confidence": confidence,
        "weights": {"individual": w_ind, "network": w_net, "ml": w_ml},
        "network_degree": net["degree"],
        "high_risk_neighbors": net["high_risk_neighbors"],
    }
    if persist:
        obj=RiskScore(risk_score_id=uuid.uuid4(), entity_type=entity_type, entity_id=entity_id, risk_score=collective, fraud_probability=float(ml["probability"]), risk_level=level, model_version=ml.get("model_version", settings.MODEL_VERSION), calculated_at=datetime.now(timezone.utc), feature_snapshot={"individual": indiv, "network": net, "ml": ml})
        db.add(obj); db.commit(); db.refresh(obj)
        result["risk_score_id"]=str(obj.risk_score_id)
    return result
