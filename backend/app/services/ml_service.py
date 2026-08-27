"""
MLPredictionService — backend facade for model/inference.
Keeps frontend -> FastAPI -> backend services -> model/inference
"""
from sqlalchemy.orm import Session
from model.inference.predict import predict_from_db as model_predict

def predict(db: Session, entity_type: str, entity_id: str):
    return model_predict(db, entity_type, entity_id)
