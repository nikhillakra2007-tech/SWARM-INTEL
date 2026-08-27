import uuid, networkx as nx
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.intelligence.graph.builder import build_graph
from app.models import FraudCluster, FraudClusterMember
from app.intelligence.risk.aggregator import collective_risk

def detect_clusters(db: Session, min_size: int=3):
    G=build_graph(db)
    comps=[c for c in nx.connected_components(G) if len(c)>=min_size]
    return comps

def cluster_risk_for_members(db: Session, members: set[str]) -> float:
    scores=[]
    for m in members:
        if m.startswith("CUSTOMER:"):
            _, eid=m.split(":",1)
            row=db.execute(text("SELECT risk_score FROM risk_scores WHERE entity_type='CUSTOMER' AND entity_id=:eid ORDER BY calculated_at DESC LIMIT 1"), {"eid": eid}).fetchone()
            if row: scores.append(float(row[0]))
    return round(sum(scores)/len(scores),2) if scores else 50

def persist_cluster(db: Session, members: set[str], cluster_ref: str | None=None) -> FraudCluster:
    # map nodes to entity_type/id
    parsed=[]
    for m in members:
        et, eid = m.split(":",1)
        parsed.append((et, eid))
    risk=cluster_risk_for_members(db, members)
    if not cluster_ref:
        # generate F-xxx
        max_ref=db.execute(text("SELECT max(cluster_ref) FROM fraud_clusters")).scalar()
        try: num=int(max_ref.split("-")[1])+1 if max_ref else 1003
        except: num=1003
        cluster_ref=f"F-{num:04d}"
    fc=FraudCluster(cluster_id=uuid.uuid4(), cluster_ref=cluster_ref, cluster_type="MIXED_ENTITY_CLUSTER", risk_score=risk, member_count=len(members), cluster_status="ACTIVE", detected_at=datetime.now(timezone.utc), last_updated_at=datetime.now(timezone.utc), _metadata={"auto": True, "method":"connected_components"})
    db.add(fc); db.flush()
    for et, eid in parsed:
        db.add(FraudClusterMember(member_id=uuid.uuid4(), cluster_id=fc.cluster_id, entity_type=et, entity_id=eid, membership_score=0.9 if et=="CUSTOMER" and risk>70 else 0.7, joined_at=datetime.now(timezone.utc)))
    db.commit(); db.refresh(fc)
    return fc
