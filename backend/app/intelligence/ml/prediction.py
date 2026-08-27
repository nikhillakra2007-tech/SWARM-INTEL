import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.intelligence.features import build_all_features
from .model_loader import load_model
from app.models import Prediction, ModelVersion
import numpy as np

def feature_vector(feats: dict) -> list:
    return [feats.get("network_degree",0), feats.get("application_count",0), feats.get("device_count",0), feats.get("shared_device_count",0), feats.get("shared_bank_account_count",0), feats.get("applications_last_7d",0), feats.get("payment_delay_average",0)]

def predict(db: Session, entity_type: str, entity_id: str):
    feats=build_all_features(db, entity_type, entity_id)
    vec=feature_vector(feats)
    model=load_model()
    if model is None:
        prob= 0.85 if feats.get("shared_device_count",0)>0 else 0.2
    else:
        try: prob=float(model.predict_proba(np.array(vec).reshape(1,-1))[0][1])
        except: prob=0.5
    return {"probability": prob, "label": "FRAUD" if prob>0.5 else "LEGIT", "features": feats}

def predict_and_store(db: Session, entity_type: str, entity_id: str):
    res=predict(db, entity_type, entity_id)
    mv=db.query(ModelVersion).filter(ModelVersion.model_status=="ACTIVE").order_by(ModelVersion.created_at.desc()).first() or db.query(ModelVersion).first()
    if not mv: raise RuntimeError("No model_version")
    obj=Prediction(prediction_id=uuid.uuid4(), model_id=mv.model_id, entity_type=entity_type, entity_id=entity_id, prediction_type="FRAUD_CLASSIFICATION", prediction_score=res["probability"], prediction_label=res["label"], feature_snapshot=res["features"], predicted_at=datetime.now(timezone.utc))
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
