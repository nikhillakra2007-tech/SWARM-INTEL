"""
Unified Analysis Orchestration Service — Phase 3 integration.
Validates entity, delegates to intelligence pipeline, returns structured result.
"""
import logging, uuid
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

log = logging.getLogger(__name__)

# Allowed entity types from DB
ALLOWED = {"CUSTOMER","DEVICE","DEALER","APPLICATION","LOAN","BANK_ACCOUNT","MOBILE","ADDRESS","GUARANTOR","IP"}

def _validate_entity(db: Session, entity_type: str, entity_id: str):
    if entity_type not in ALLOWED:
        raise HTTPException(400, f"Unsupported entity_type {entity_type}. Allowed: {sorted(ALLOWED)}")
    try:
        uuid.UUID(entity_id)
    except:
        raise HTTPException(400, f"Invalid UUID for {entity_type}: {entity_id}")
    # Check existence for primary entities
    table_map = {
        "CUSTOMER": ("customers","customer_id"),
        "DEVICE": ("devices","device_id"),
        "DEALER": ("dealers","dealer_id"),
        "APPLICATION": ("loan_applications","application_id"),
        "LOAN": ("loans","loan_id"),
    }
    if entity_type in table_map:
        tbl, col = table_map[entity_type]
        exists = db.execute(text(f"SELECT 1 FROM {tbl} WHERE {col}=:eid LIMIT 1"), {"eid": entity_id}).scalar()
        if not exists:
            raise HTTPException(404, f"{entity_type} {entity_id} not found")

def analyze_entity(db: Session, entity_type: str, entity_id: str, persist: bool=True) -> dict:
    log.info("ANALYSIS START %s %s", entity_type, entity_id)
    _validate_entity(db, entity_type, entity_id)
    # 1-9: intelligence
    from app.intelligence.pipeline import full_analysis
    try:
        result = full_analysis(db, entity_type, entity_id, persist=persist)
    except FileNotFoundError as e:
        # model artifact missing
        log.error("Model artifact missing: %s", e)
        raise HTTPException(503, f"Model artifact unavailable: {e}")
    except ValueError as e:
        # feature schema mismatch
        log.error("Feature schema error: %s", e)
        raise HTTPException(422, str(e))
    except Exception as e:
        log.exception("Analysis failed")
        raise HTTPException(500, f"Analysis failed: {str(e)[:300]}")

    # Enrich with cluster info
    cluster_info = None
    try:
        from sqlalchemy import text as t
        row = db.execute(t("SELECT fc.cluster_ref, fc.risk_score, fc.member_count, fc.cluster_status FROM fraud_clusters fc JOIN fraud_cluster_members fcm ON fcm.cluster_id=fc.cluster_id WHERE fcm.entity_id=:eid LIMIT 1"), {"eid": entity_id}).fetchone()
        if row:
            cluster_info = {"cluster_ref": row[0], "risk_score": float(row[1]) if row[1] else None, "member_count": row[2], "status": row[3]}
    except: pass

    # Build structured response for frontend (keeps original keys for backward compat + new)
    structured = {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "individual_risk": {"score": result["collective"]["individual_risk_score"], "level": result["collective"]["individual_level"]},
        "network_risk": {"score": result["collective"]["network_risk_score"], "level": result["collective"]["network_level"]},
        "ml_prediction": {"fraud_probability": result["ml"]["probability"], "prediction": result["ml"]["label"], "model_version": result["ml"].get("model_version","unknown") if isinstance(result["ml"], dict) else result["collective"].get("model_version"), "threshold": 0.3},
        "collective_risk": {"score": result["collective"]["collective_risk_score"], "level": result["collective"]["risk_level"], "confidence": result["collective"]["confidence"], "weights": result["collective"]["weights"]},
        "signals": result["rules"],
        "anomalies": result["anomaly"],
        "temporal": result["temporal"],
        "network": result["graph"],
        "cluster": cluster_info,
        "evidence": result["explanation"]["reasons"],
        "alert": result["alert"],
        "feature_schema": list(result["features"].keys()) if isinstance(result["features"], dict) else [],
        # backward compat keys
        "collective": result["collective"],
        "explanation": result["explanation"],
        "features": result["features"],
        "rules": result["rules"],
        "graph": result["graph"],
        "anomaly": result["anomaly"],
        "ml": result["ml"],
        "temporal": result["temporal"],
    }
    log.info("ANALYSIS COMPLETE %s collective=%s", entity_id, structured["collective_risk"]["score"])
    return structured
