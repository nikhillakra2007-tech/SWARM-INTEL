import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.intelligence.rules.engine import run_rules
from app.intelligence.anomaly.detector import anomaly_score_isolation
from app.intelligence.ml.prediction import predict
from app.intelligence.features import build_all_features
from app.models import RiskScore

def risk_level(score: float) -> str:
    if score<30: return "LOW"
    if score<60: return "MEDIUM"
    if score<80: return "HIGH"
    return "CRITICAL"

def individual_risk(db: Session, entity_type: str, entity_id: str) -> dict:
    rules=run_rules(db, entity_type, entity_id)
    max_rule=max([r["score"] for r in rules], default=0)
    # individual: only non-network rules
    indiv_rules=[r for r in rules if r["signal_type"] not in ("HIGH_NETWORK_CONNECTIVITY","RAPID_CLUSTER_GROWTH")]
    indiv_score=max([r["score"] for r in indiv_rules], default=20) if indiv_rules else 15
    return {"score": float(indiv_score), "level": risk_level(indiv_score), "top_signals": indiv_rules[:2]}

def network_risk(db: Session, entity_type: str, entity_id: str) -> dict:
    """
    Network risk is PURE network intelligence:
    - shared entity rules (device/mobile/bank/address/guarantor)
    - connectivity (degree, high-risk neighbors, density)
    Does NOT include ML or anomaly to avoid double counting (see aggregator doc).
    """
    from app.intelligence.graph.analysis import suspicious_connectivity
    rules=run_rules(db, entity_type, entity_id)
    net_rules=[r for r in rules if r["signal_type"] in ("SHARED_DEVICE","SHARED_MOBILE","SHARED_BANK_ACCOUNT","SHARED_ADDRESS","SHARED_GUARANTOR","HIGH_NETWORK_CONNECTIVITY","RAPID_CLUSTER_GROWTH","SAME_IP")]
    max_net=max([r["score"] for r in net_rules], default=0)
    conn=suspicious_connectivity(db, entity_type, entity_id)
    # density via ego graph
    try:
        from app.intelligence.graph.metrics import density_of_ego
        density=density_of_ego(db, entity_type, entity_id, depth=1)
    except: density=0
    density_boost = density * 15  # 0-15
    net_score=min(100, max_net*0.6 + conn["degree"]*3 + hr_boost(conn) + density_boost)
    if not net_rules and conn["degree"]<2:
        net_score=min(net_score, 25)
    return {"score": round(float(net_score),2), "level": risk_level(net_score), "degree": conn["degree"], "high_risk_neighbors": conn["high_risk_neighbors"], "density": density}

def hr_boost(conn): return min(15, conn["high_risk_neighbors"]*7)
