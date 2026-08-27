from sqlalchemy.orm import Session
from app.ml.features.engine import build_features
from app.ml.models.baseline import load_model, predict_proba
from app.models import Prediction, ModelVersion
import uuid
from datetime import datetime, timezone

def predict(db: Session, entity_type: str, entity_id: str):
    feats = build_features(db, entity_type, entity_id)
    vec = [feats.get("degree",0), feats.get("application_count",0), feats.get("device_count",0), feats.get("shared_device_count",0), feats.get("bank_count",0)]
    model = load_model()
    prob = predict_proba(model, vec) if model else (0.85 if feats.get("shared_device_count",0)>0 else 0.2)
    return {"probability": prob, "features": feats}

def predict_and_store(db: Session, entity_type: str, entity_id: str):
    result = predict(db, entity_type, entity_id)
    mv = db.query(ModelVersion).filter(ModelVersion.model_status=="ACTIVE").order_by(ModelVersion.created_at.desc()).first()
    if not mv:
        mv = db.query(ModelVersion).first()
    if not mv:
        raise RuntimeError("No model_version available")
    obj = Prediction(prediction_id=uuid.uuid4(), model_id=mv.model_id, entity_type=entity_type, entity_id=entity_id, prediction_type="FRAUD_CLASSIFICATION", prediction_score=result["probability"], prediction_label="FRAUD" if result["probability"]>0.5 else "LEGIT", feature_snapshot=result["features"], predicted_at=datetime.now(timezone.utc))
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
