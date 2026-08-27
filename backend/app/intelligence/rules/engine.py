from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
import uuid
from .rules import ALL_RULES
from app.models import FraudSignal

def run_rules(db: Session, entity_type: str, entity_id: str) -> list[dict]:
    signals=[]
    for fn in ALL_RULES:
        try:
            res = fn(db, entity_type, entity_id)
            if res:
                res.setdefault("entity_type", entity_type)
                res.setdefault("entity_id", entity_id)
                signals.append(res)
        except Exception as e:
            # log but continue
            import logging; logging.getLogger(__name__).warning("rule %s failed: %s", fn.__name__, e)
    return signals

def persist(db: Session, signals: list[dict]) -> list[FraudSignal]:
    objs=[]
    for s in signals:
        obj = FraudSignal(
            signal_id=uuid.uuid4(),
            entity_type=s["entity_type"], entity_id=s["entity_id"],
            signal_type=s["signal_type"], severity=s["severity"],
            score=s["score"], confidence=s["confidence"],
            description=s["explanation"], detected_at=datetime.now(timezone.utc),
            evidence=s.get("evidence",{})
        )
        db.add(obj); objs.append(obj)
    db.commit()
    return objs

def analyze_and_persist(db: Session, entity_type: str, entity_id: str, persist: bool=False):
    sigs = run_rules(db, entity_type, entity_id)
    if persist and sigs:
        persist(db, sigs)
    return sigs
