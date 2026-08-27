from sqlalchemy.orm import Session
from app.intelligence.features import build_all_features
from app.intelligence.rules.engine import run_rules, persist as persist_rules
from app.intelligence.graph.builder import build_graph
from app.intelligence.anomaly.detector import anomaly_score_isolation
from app.intelligence.ml.prediction import predict, predict_and_store
from app.intelligence.temporal.analyzer import growth_analysis
from app.intelligence.risk.aggregator import collective_risk
from app.intelligence.risk.explanation import explain
from app.intelligence.clustering.detector import detect_clusters
import uuid

def full_analysis(db: Session, entity_type: str, entity_id: str, persist: bool=True) -> dict:
    feats=build_all_features(db, entity_type, entity_id)
    rules=run_rules(db, entity_type, entity_id)
    if persist and rules:
        persist_rules(db, rules)
    # graph already via build_graph
    G=build_graph(db)
    node=f"{entity_type}:{entity_id}"
    graph_info={"in_graph": node in G, "degree": int(G.degree(node)) if node in G else 0}
    anomaly=anomaly_score_isolation(db, entity_type, entity_id)
    ml=predict(db, entity_type, entity_id)
    if persist:
        try: predict_and_store(db, entity_type, entity_id)
        except: pass
    temporal=growth_analysis(db, entity_type, entity_id)
    collective=collective_risk(db, entity_type, entity_id, persist=persist)
    explanation=explain(db, entity_type, entity_id, collective)
    # alert if collective high
    alert=None
    if collective["collective_risk_score"]>=70 or collective["network_risk_score"]>=75:
        from app.models import FraudAlert
        from datetime import datetime, timezone
        alert_ref=f"ALT-{uuid.uuid4().hex[:4].upper()}"
        # avoid duplicate: check existing open alert
        existing=db.query(FraudAlert).filter(FraudAlert.entity_type==entity_type, FraudAlert.entity_id==entity_id, FraudAlert.alert_status.in_(["OPEN","ACKNOWLEDGED","IN_INVESTIGATION"])).first()
        if not existing:
            alert=FraudAlert(alert_id=uuid.uuid4(), alert_ref=alert_ref, entity_type=entity_type, entity_id=entity_id, alert_type="EMERGING_FRAUD_NETWORK" if temporal["is_rapid_growth"] else "HIGH_RISK_DEVICE_CLUSTER", severity="CRITICAL" if collective["risk_level"]=="CRITICAL" else "HIGH", risk_score=collective["collective_risk_score"], alert_status="OPEN", generated_at=datetime.now(timezone.utc), evidence={"collective": collective, "rules": len(rules)})
            db.add(alert); db.commit(); db.refresh(alert)
            alert={"alert_id": str(alert.alert_id), "alert_ref": alert.alert_ref, "severity": alert.severity}
    return {
        "entity_type": entity_type, "entity_id": entity_id,
        "features": feats, "rules": rules, "graph": graph_info,
        "anomaly": anomaly, "ml": ml, "temporal": temporal,
        "collective": collective, "explanation": explanation, "alert": alert
    }
