from sqlalchemy import text
from sqlalchemy.orm import Session
from app.intelligence.graph.engine import build_graph

def network_features(db: Session, entity_type: str, entity_id: str) -> dict:
    G = build_graph(db)
    node = f"{entity_type}:{entity_id}"
    degree = int(G.degree(node)) if node in G else 0
    # shared counts via relationships table (targeted queries for speed)
    q = lambda sql: db.execute(text(sql), {"eid": entity_id, "etype": entity_type}).scalar() or 0
    # for CUSTOMER, count distinct shared
    shared_device = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_DEVICE' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    shared_mobile = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_MOBILE' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    shared_bank = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_BANK_ACCOUNT' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    shared_addr = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_ADDRESS' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    shared_guar = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_GUARANTOR' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    # unique connected customers via 1-hop shared
    try:
        from app.intelligence.graph.engine import neighbors
        sub = neighbors(db, entity_type, entity_id, depth=1)
        connected_customers = len([n for n in sub.get("nodes",[]) if n.get("entity_type")=="CUSTOMER"]) - (1 if entity_type=="CUSTOMER" else 0)
        # network density of ego graph
        ego_nodes = len(sub.get("nodes",[]))
        ego_edges = len(sub.get("edges",[]))
        density = (2*ego_edges)/(ego_nodes*(ego_nodes-1)) if ego_nodes>1 else 0
        # high-risk neighbor count
        high_risk = 0
        if connected_customers>0:
            ids = [n["entity_id"] for n in sub["nodes"] if n.get("entity_type")=="CUSTOMER" and n["entity_id"]!=entity_id]
            if ids:
                # ids are strings, cast to uuid for query
                rows = db.execute(text("SELECT count(DISTINCT entity_id) FROM risk_scores WHERE entity_type='CUSTOMER' AND entity_id::text = ANY(:ids) AND risk_level IN ('HIGH','CRITICAL') AND calculated_at = (SELECT max(calculated_at) FROM risk_scores rs2 WHERE rs2.entity_id=risk_scores.entity_id)"), {"ids": ids}).scalar() or 0
                high_risk = int(rows)
        # cluster size via fraud_cluster_members if any
        cluster_size = int(db.execute(text("SELECT coalesce(max(member_count),0) FROM fraud_clusters fc JOIN fraud_cluster_members fcm ON fcm.cluster_id=fc.cluster_id WHERE fcm.entity_id=:eid"), {"eid": entity_id}).scalar() or 0)
    except Exception:
        connected_customers = 0; density = 0; high_risk = 0; cluster_size = 0
    dealer_conn = int(db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SAME_DEALER' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0) if entity_type=="CUSTOMER" else 0
    return {
        "network_degree": degree,
        "unique_connected_customers": int(connected_customers),
        "shared_device_count": shared_device,
        "shared_mobile_count": shared_mobile,
        "shared_bank_account_count": shared_bank,
        "shared_address_count": shared_addr,
        "shared_guarantor_count": shared_guar,
        "dealer_connectivity": dealer_conn,
        "high_risk_neighbor_count": int(high_risk),
        "cluster_size": int(cluster_size),
        "network_density": round(float(density), 4),
    }
