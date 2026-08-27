from sqlalchemy import text
from sqlalchemy.orm import Session
from app.intelligence.graph.engine import build_graph

def rule_shared_device(db: Session, entity_type: str, entity_id: str):
    cnt = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_DEVICE' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    if cnt>0:
        return {"signal_type":"SHARED_DEVICE","severity":"CRITICAL","score":min(95,60+int(cnt)*15+10),"confidence":0.95 if cnt>=2 else 0.8,"explanation":f"Device shared with {cnt} entities — cross-customer device reuse","evidence":{"shared_device_count":int(cnt)}}

def rule_identity_reuse(db: Session, entity_type: str, entity_id: str):
    # guarantor reuse as proxy for identity reuse
    cnt = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_GUARANTOR' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    # also check multiple mobiles as identity reuse
    if entity_type=="CUSTOMER":
        mc = db.execute(text("SELECT count(*) FROM customer_mobile_links WHERE customer_id=:eid"), {"eid": entity_id}).scalar() or 0
        if int(mc)>=3:
            return {"signal_type":"IDENTITY_REUSE","severity":"HIGH","score":78,"confidence":0.82,"explanation":f"Customer linked to {mc} mobiles — possible identity reuse","evidence":{"mobile_count":int(mc)}}
    if cnt>0:
        return {"signal_type":"IDENTITY_REUSE","severity":"HIGH","score":80,"confidence":0.85,"explanation":f"Guarantor/identity linked across {cnt} relationships","evidence":{"shared_guarantor_count":int(cnt)}}

def rule_multiple_mobile(db: Session, entity_type: str, entity_id: str):
    if entity_type!="CUSTOMER": return None
    cnt = db.execute(text("SELECT count(*) FROM customer_mobile_links WHERE customer_id=:eid"), {"eid": entity_id}).scalar() or 0
    # also shared mobile via graph
    shared = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_MOBILE' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    if int(shared)>0:
        return {"signal_type":"SHARED_MOBILE","severity":"CRITICAL","score":88,"confidence":0.9,"explanation":f"Mobile shared with {shared} entities — collision","evidence":{"shared_mobile_count":int(shared)}}
    if int(cnt)>=3:
        return {"signal_type":"MULTIPLE_MOBILE_LINK","severity":"MEDIUM","score":65,"confidence":0.7,"explanation":f"{cnt} mobiles linked to single customer","evidence":{"mobile_count":int(cnt)}}

def rule_multiple_bank(db: Session, entity_type: str, entity_id: str):
    if entity_type!="CUSTOMER": return None
    shared = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_BANK_ACCOUNT' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    if int(shared)>0:
        return {"signal_type":"MULTIPLE_BANK_ACCOUNT_LINK","severity":"CRITICAL","score":90,"confidence":0.93,"explanation":f"Bank account shared across {shared} relationships — financial link","evidence":{"shared_bank_count":int(shared)}}

def rule_shared_address(db: Session, entity_type: str, entity_id: str):
    cnt = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_ADDRESS' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    if cnt>0:
        return {"signal_type":"SHARED_ADDRESS","severity":"HIGH","score":80,"confidence":0.82,"explanation":f"Address shared with {cnt} entities","evidence":{"shared_address_count":int(cnt)}}

def rule_shared_guarantor(db: Session, entity_type: str, entity_id: str):
    cnt = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SHARED_GUARANTOR' AND (source_entity_id=:eid OR target_entity_id=:eid)"), {"eid": entity_id}).scalar() or 0
    if cnt>0:
        return {"signal_type":"SHARED_GUARANTOR","severity":"HIGH","score":85,"confidence":0.87,"explanation":f"Guarantor shared across {cnt} relationships","evidence":{"shared_guarantor_count":int(cnt)}}

def rule_same_ip(db: Session, entity_type: str, entity_id: str):
    cnt = db.execute(text("SELECT count(*) FROM entity_relationships WHERE relationship_type='SAME_IP' AND (source_entity_type=:etype AND source_entity_id=:eid OR target_entity_type=:etype AND target_entity_id=:eid)"), {"eid": entity_id, "etype": entity_type}).scalar() or 0
    # also via DEVICE->IP edges
    if entity_type=="CUSTOMER":
        cnt2 = db.execute(text("SELECT count(*) FROM entity_relationships er JOIN customer_device_links cdl ON cdl.customer_id=:eid AND (er.source_entity_id=cdl.device_id OR er.target_entity_id=cdl.device_id) WHERE er.relationship_type='SAME_IP'"), {"eid": entity_id}).scalar() or 0
        cnt = max(int(cnt), int(cnt2))
    if cnt>0:
        return {"signal_type":"SAME_IP","severity":"MEDIUM","score":70,"confidence":0.75,"explanation":f"IP overlaps with {cnt} entities — possible co-location","evidence":{"same_ip_count":int(cnt)}}

def rule_dealer_cluster(db: Session, entity_type: str, entity_id: str):
    # if customer linked to high-velocity dealer
    if entity_type=="CUSTOMER":
        row = db.execute(text("SELECT d.dealer_code, count(*) as cnt FROM loan_applications la JOIN dealers d ON d.dealer_id=la.dealer_id WHERE d.dealer_id IN (SELECT dealer_id FROM loan_applications WHERE customer_id=:eid) GROUP BY d.dealer_code HAVING count(*)>3"), {"eid": entity_id}).fetchone()
        if row:
            return {"signal_type":"UNUSUAL_DEALER_CLUSTER","severity":"CRITICAL","score":94,"confidence":0.96,"explanation":f"Dealer {row[0]} has {row[1]} applications in burst — unusual cluster","evidence":{"dealer_code":row[0],"dealer_apps":int(row[1])}}
    if entity_type=="DEALER":
        cnt = db.execute(text("SELECT count(*) FROM loan_applications WHERE dealer_id=:eid AND application_timestamp > now() - interval '7 days'"), {"eid": entity_id}).scalar() or 0
        if int(cnt)>=4:
            return {"signal_type":"UNUSUAL_DEALER_CLUSTER","severity":"CRITICAL","score":92,"confidence":0.94,"explanation":f"Dealer burst {cnt} apps in 7 days vs baseline 2/month","evidence":{"recent_apps":int(cnt)}}

def rule_location_anomaly(db: Session, entity_type: str, entity_id: str):
    if entity_type!="CUSTOMER": return None
    cnt = db.execute(text("SELECT count(DISTINCT location_id) FROM application_events WHERE customer_id=:eid"), {"eid": entity_id}).scalar() or 0
    if int(cnt)>=3:
        return {"signal_type":"LOCATION_ANOMALY","severity":"MEDIUM","score":68,"confidence":0.7,"explanation":f"Events across {cnt} distinct locations — movement anomaly","evidence":{"distinct_locations":int(cnt)}}

def rule_rapid_burst(db: Session, entity_type: str, entity_id: str):
    if entity_type=="CUSTOMER":
        cnt = db.execute(text("SELECT count(*) FROM loan_applications WHERE customer_id=:eid AND application_timestamp > now() - interval '7 days'"), {"eid": entity_id}).scalar() or 0
        if int(cnt)>=2:
            return {"signal_type":"RAPID_APPLICATION_BURST","severity":"HIGH","score":85,"confidence":0.85,"explanation":f"{cnt} applications in 7 days — burst","evidence":{"apps_7d":int(cnt)}}
        cnt24 = db.execute(text("SELECT count(*) FROM loan_applications WHERE customer_id=:eid AND application_timestamp > now() - interval '24 hours'"), {"eid": entity_id}).scalar() or 0
        if int(cnt24)>=2:
            return {"signal_type":"RAPID_APPLICATION_BURST","severity":"CRITICAL","score":89,"confidence":0.9,"explanation":f"{cnt24} applications in 24h — rapid burst","evidence":{"apps_24h":int(cnt24)}}

def rule_repayment(db: Session, entity_type: str, entity_id: str):
    loan_id = None
    if entity_type=="LOAN": loan_id = entity_id
    elif entity_type=="CUSTOMER":
        row = db.execute(text("SELECT l.loan_id FROM loans l JOIN loan_applications la ON la.application_id=l.application_id WHERE la.customer_id=:eid LIMIT 1"), {"eid": entity_id}).fetchone()
        if row: loan_id = str(row[0])
    if loan_id:
        row = db.execute(text("SELECT bounce_count, missed_payment_count, partial_payment_count FROM repayment_behaviour WHERE loan_id=:lid ORDER BY calculated_at DESC LIMIT 1"), {"lid": loan_id}).fetchone()
        if row and (row[0]>0 or row[1]>0):
            return {"signal_type":"UNUSUAL_REPAYMENT_PATTERN","severity":"HIGH","score":85,"confidence":0.88,"explanation":f"Bounces {row[0]}, misses {row[1]}, partials {row[2]} — repayment anomaly","evidence":{"bounce_count":int(row[0]),"missed":int(row[1])}}

def rule_high_connectivity(db: Session, entity_type: str, entity_id: str):
    from app.intelligence.graph.engine import build_graph
    G = build_graph(db)
    node = f"{entity_type}:{entity_id}"
    if node in G and G.degree(node)>=4:
        return {"signal_type":"HIGH_NETWORK_CONNECTIVITY","severity":"HIGH","score":80,"confidence":0.8,"explanation":f"Network degree {G.degree(node)} — highly connected","evidence":{"degree":int(G.degree(node))}}

def rule_rapid_cluster_growth(db: Session, entity_type: str, entity_id: str):
    # if in cluster with recent growth
    row = db.execute(text("SELECT fc.cluster_ref, count(*) FILTER (WHERE fcm.joined_at > now()-interval '7 days') as newc FROM fraud_clusters fc JOIN fraud_cluster_members fcm ON fcm.cluster_id=fc.cluster_id WHERE fcm.entity_id=:eid GROUP BY fc.cluster_ref HAVING count(*) FILTER (WHERE fcm.joined_at > now()-interval '7 days') >=2"), {"eid": entity_id}).fetchone()
    if row:
        return {"signal_type":"RAPID_CLUSTER_GROWTH","severity":"HIGH","score":82,"confidence":0.84,"explanation":f"Cluster {row[0]} grew by {row[1]} in 7 days — rapid expansion","evidence":{"cluster_ref":row[0],"new_members":int(row[1])}}

ALL_RULES = [
    rule_shared_device, rule_identity_reuse, rule_multiple_mobile, rule_multiple_bank,
    rule_shared_address, rule_shared_guarantor, rule_same_ip, rule_dealer_cluster,
    rule_location_anomaly, rule_rapid_burst, rule_repayment, rule_high_connectivity, rule_rapid_cluster_growth
]
