from sqlalchemy.orm import Session
from app.intelligence.rules.engine import run_rules
from app.intelligence.anomaly.detector import anomaly_score_isolation
from app.intelligence.ml.prediction import predict
from app.intelligence.graph.analysis import suspicious_connectivity
from app.intelligence.temporal.analyzer import growth_analysis

def explain(db: Session, entity_type: str, entity_id: str, collective: dict) -> dict:
    rules=run_rules(db, entity_type, entity_id)
    anomaly=anomaly_score_isolation(db, entity_type, entity_id)
    ml=predict(db, entity_type, entity_id)
    conn=suspicious_connectivity(db, entity_type, entity_id)
    temp=growth_analysis(db, entity_type, entity_id)
    reasons=[]
    for r in sorted(rules, key=lambda x: x["score"], reverse=True)[:5]:
        reasons.append(f"{r['signal_type']} — {r['explanation']} (score {r['score']})")
    if anomaly["is_anomaly"]:
        reasons.append(f"Behaviour anomaly detected (score {anomaly['anomaly_score']}, method {anomaly['method']})")
    reasons.append(f"ML fraud probability = {ml['probability']:.2f} ({ml['label']})")
    if conn["suspicious"]:
        reasons.append(f"Network degree {conn['degree']} with {conn['high_risk_neighbors']} high-risk neighbors — suspicious connectivity")
    if temp["is_rapid_growth"]:
        reasons.append(f"Rapid growth: +{temp['new_connections_last_7d']} connections in 7d, net growth rate {temp['network_growth_rate']}")
    if not reasons:
        reasons=["No strong signals — appears normal"]
    return {
        "collective_risk_score": collective.get("collective_risk_score"),
        "risk_level": collective.get("risk_level"),
        "individual_risk_score": collective.get("individual_risk_score"),
        "network_risk_score": collective.get("network_risk_score"),
        "fraud_probability": collective.get("fraud_probability"),
        "reasons": reasons,
        "evidence": {"rules": rules, "anomaly": anomaly, "ml": ml, "connectivity": conn, "temporal": temp}
    }
