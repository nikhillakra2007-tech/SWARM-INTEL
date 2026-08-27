"""Backward compat — delegates to intelligence.risk"""
from app.intelligence.risk.aggregator import collective_risk
def calculate_risk(db, entity_type, entity_id, model_version=None):
    res=collective_risk(db, entity_type, entity_id, persist=True)
    # return RiskScore-like object shim: fetch last
    from app.models import RiskScore
    obj=db.query(RiskScore).filter(RiskScore.entity_type==entity_type, RiskScore.entity_id==entity_id).order_by(RiskScore.calculated_at.desc()).first()
    from app.intelligence.rules.engine import run_rules
    signals=run_rules(db, entity_type, entity_id)
    return obj, signals
