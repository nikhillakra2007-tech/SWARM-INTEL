from sqlalchemy.orm import Session
from app.intelligence.pipeline import full_analysis
from app.intelligence.features import build_all_features
from app.intelligence.risk.aggregator import collective_risk
from app.intelligence.risk.explanation import explain
from app.intelligence.temporal.analyzer import growth_analysis

def analyze(db: Session, entity_type: str, entity_id: str): return full_analysis(db, entity_type, entity_id)
def features(db: Session, entity_type: str, entity_id: str): return build_all_features(db, entity_type, entity_id)
def risk(db: Session, entity_type: str, entity_id: str): return collective_risk(db, entity_type, entity_id, persist=False)
