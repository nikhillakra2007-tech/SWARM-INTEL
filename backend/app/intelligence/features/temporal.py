from sqlalchemy import text
from sqlalchemy.orm import Session

def temporal_features(db: Session, entity_type: str, entity_id: str) -> dict:
    if entity_type != "CUSTOMER":
        # generic: new connections
        new_24h = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE (source_entity_id=:eid OR target_entity_id=:eid) AND first_seen > now() - interval '24 hours'"), {"eid": entity_id}).scalar() or 0)
        new_7d = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE (source_entity_id=:eid OR target_entity_id=:eid) AND first_seen > now() - interval '7 days'"), {"eid": entity_id}).scalar() or 0)
        return {"applications_last_24h": 0, "applications_last_7d": 0, "new_connections_last_24h": new_24h, "new_connections_last_7d": new_7d, "cluster_growth_rate": 0, "network_growth_rate": 0, "risk_score_change": 0}
    apps_24h = int(db.execute(text("SELECT count(*) FROM loan_applications WHERE customer_id=:eid AND application_timestamp > now() - interval '24 hours'"), {"eid": entity_id}).scalar() or 0)
    apps_7d = int(db.execute(text("SELECT count(*) FROM loan_applications WHERE customer_id=:eid AND application_timestamp > now() - interval '7 days'"), {"eid": entity_id}).scalar() or 0)
    new_conn_24h = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE (source_entity_id=:eid OR target_entity_id=:eid) AND first_seen > now() - interval '24 hours'"), {"eid": entity_id}).scalar() or 0)
    new_conn_7d = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE (source_entity_id=:eid OR target_entity_id=:eid) AND first_seen > now() - interval '7 days'"), {"eid": entity_id}).scalar() or 0)
    # cluster growth if in cluster: members joined last 7d vs before
    cluster_growth = db.execute(text("SELECT count(*) FILTER (WHERE joined_at > now()-interval '7 days')::float / NULLIF(count(*) FILTER (WHERE joined_at <= now()-interval '7 days'),0) FROM fraud_cluster_members WHERE entity_id=:eid"), {"eid": entity_id}).scalar() or 0
    # network growth rate = new_7d / max(1, total- new_7d)
    total_conn = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE source_entity_id=:eid OR target_entity_id=:eid"), {"eid": entity_id}).scalar() or 0)
    net_growth = round(new_conn_7d / max(1, total_conn - new_conn_7d + 1), 3) if total_conn else 0
    # risk change
    scores = db.execute(text("SELECT risk_score FROM risk_scores WHERE entity_type='CUSTOMER' AND entity_id=:eid ORDER BY calculated_at DESC LIMIT 2"), {"eid": entity_id}).fetchall()
    risk_change = round(float(scores[0][0]) - float(scores[1][0]),2) if len(scores)==2 else 0
    return {
        "applications_last_24h": apps_24h,
        "applications_last_7d": apps_7d,
        "new_connections_last_24h": new_conn_24h,
        "new_connections_last_7d": new_conn_7d,
        "cluster_growth_rate": round(float(cluster_growth or 0),3),
        "network_growth_rate": net_growth,
        "risk_score_change": risk_change,
    }
