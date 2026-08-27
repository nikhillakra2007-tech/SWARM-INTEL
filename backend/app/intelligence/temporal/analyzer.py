from sqlalchemy import text
from sqlalchemy.orm import Session

def temporal_profile(db: Session, entity_type: str, entity_id: str) -> dict:
    from app.intelligence.features.temporal import temporal_features
    return temporal_features(db, entity_type, entity_id)

def growth_analysis(db: Session, entity_type: str, entity_id: str) -> dict:
    prof=temporal_profile(db, entity_type, entity_id)
    is_rapid = prof.get("new_connections_last_7d",0)>=3 or prof.get("applications_last_7d",0)>=2 or prof.get("network_growth_rate",0)>0.5
    return {**prof, "is_rapid_growth": bool(is_rapid), "emerging_risk": "HIGH" if is_rapid and prof.get("risk_score_change",0)>15 else "LOW"}

def cluster_growth(db: Session, cluster_id: str) -> dict:
    total=int(db.execute(text("SELECT count(*) FROM fraud_cluster_members WHERE cluster_id=:cid AND left_at IS NULL"), {"cid": cluster_id}).scalar() or 0)
    new7=int(db.execute(text("SELECT count(*) FROM fraud_cluster_members WHERE cluster_id=:cid AND joined_at > now()-interval '7 days'"), {"cid": cluster_id}).scalar() or 0)
    old=total-new7
    rate= round(new7/max(1,old),3) if old else (new7 if new7 else 0)
    return {"total": total, "new_7d": new7, "old": old, "growth_rate": rate, "is_rapid": rate>0.5 or new7>=3}
