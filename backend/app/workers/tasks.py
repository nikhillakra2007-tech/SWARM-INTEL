"""Background task foundation — ready for future continuous intelligence.
Current stage: synchronous services; later can plug Celery/ARQ without API changes.
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.fraud.signals.engine import analyze_entity, persist_signals
from app.fraud.scoring.engine import calculate_risk
from app.utils.logging import get_logger

log = get_logger(__name__)

def run_pipeline_for_application(application_id: str):
    """Conceptual pipeline: New app -> relationships -> fraud -> risk -> cluster -> alert
    Currently synchronous; offload to background task queue later.
    """
    db: Session = SessionLocal()
    try:
        log.info("pipeline start for app %s", application_id)
        # placeholder — would update entity_relationships, then:
        # signals = analyze_entity(...)
        # risk, _ = calculate_risk(...)
        log.info("pipeline done for app %s", application_id)
    finally:
        db.close()
