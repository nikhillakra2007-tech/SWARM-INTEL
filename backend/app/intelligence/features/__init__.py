from .customer import customer_features
from .network import network_features
from .behaviour import behaviour_features
from .temporal import temporal_features
from sqlalchemy.orm import Session

def build_all_features(db: Session, entity_type: str, entity_id: str) -> dict:
    feats = {}
    if entity_type == "CUSTOMER":
        feats.update(customer_features(db, entity_id))
        feats.update(behaviour_features(db, entity_id))
    feats.update(network_features(db, entity_type, entity_id))
    feats.update(temporal_features(db, entity_type, entity_id))
    # compat keys for older ml
    feats.setdefault("degree", feats.get("network_degree",0))
    feats.setdefault("shared_device_count", feats.get("shared_device_count",0))
    feats.setdefault("application_count", feats.get("application_count",0))
    return feats
