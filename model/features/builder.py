"""
Feature extraction for ML — reuses intelligence layer but restricts to leakage-free pre-fraud features.
All features are available at prediction time (counts, network degree, recent behavior, repayment delay) without using future labels like risk_scores or cluster fraud status.
"""
import sys, pathlib
# Allow model to be imported from both swarm/ and swarm/backend contexts
for p in [pathlib.Path(__file__).parents[2], pathlib.Path(__file__).parents[2] / "backend"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from sqlalchemy.orm import Session
from app.intelligence.features import build_all_features
from .schema import FEATURE_SCHEMA

def extract_features(db: Session, entity_type: str, entity_id: str) -> dict:
    all_feats = build_all_features(db, entity_type, entity_id)
    # Project to schema in deterministic order
    return {k: float(all_feats.get(k, 0)) for k in FEATURE_SCHEMA}

def vectorize(features: dict) -> list[float]:
    return [float(features[k]) for k in FEATURE_SCHEMA]
