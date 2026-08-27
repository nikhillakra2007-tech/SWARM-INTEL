from sqlalchemy.orm import Session
from app.intelligence.features import build_all_features

def anomaly_feature_vector(db: Session, entity_type: str, entity_id: str) -> list[float]:
    feats=build_all_features(db, entity_type, entity_id)
    # numeric vector for IsolationForest
    keys=["network_degree","application_count" if "application_count" in feats else "degree","shared_device_count","shared_bank_account_count","applications_last_7d","new_connections_last_7d","payment_delay_average","missed_payment_count"]
    vec=[]
    for k in keys:
        v=feats.get(k,0)
        try: vec.append(float(v))
        except: vec.append(0)
    return vec

def feature_matrix_for_customers(db: Session, limit: int = 500):
    from sqlalchemy import text
    import random
    rows=db.execute(text("SELECT customer_id FROM customers")).fetchall()
    if len(rows) > limit:
        rows = random.sample(rows, limit)
    X=[anomaly_feature_vector(db,"CUSTOMER",str(r[0])) for r in rows]
    ids=[str(r[0]) for r in rows]
    return ids, X
