from sqlalchemy import text
from sqlalchemy.orm import Session
from .builder import build_graph
from .metrics import degree
from app.models import RiskScore

def high_risk_neighbors(db: Session, entity_type: str, entity_id: str, depth: int=1) -> int:
    from .traversal import bfs_nodes
    G=build_graph(db)
    nodes=bfs_nodes(G, f"{entity_type}:{entity_id}", depth)
    cust_ids=[n.split(":",1)[1] for n in nodes if n.startswith("CUSTOMER:") and n!=f"{entity_type}:{entity_id}"]
    if not cust_ids: return 0
    q=text("SELECT count(*) FROM risk_scores WHERE entity_type='CUSTOMER' AND entity_id::text = ANY(:ids) AND risk_level IN ('HIGH','CRITICAL') AND calculated_at = (SELECT max(calculated_at) FROM risk_scores rs2 WHERE rs2.entity_id=risk_scores.entity_id)")
    return int(db.execute(q, {"ids": cust_ids}).scalar() or 0)

def suspicious_connectivity(db: Session, entity_type: str, entity_id: str) -> dict:
    deg=degree(db, entity_type, entity_id)
    hr=high_risk_neighbors(db, entity_type, entity_id)
    total=int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE source_entity_id=:eid OR target_entity_id=:eid"), {"eid": entity_id}).scalar() or 0)
    growth=int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE (source_entity_id=:eid OR target_entity_id=:eid) AND first_seen > now()-interval '7 days'"), {"eid": entity_id}).scalar() or 0)
    return {"degree":deg,"high_risk_neighbors":hr,"total_connections":total,"new_connections_7d":growth,"suspicious": hr>=2 or deg>=5 or growth>=3}
