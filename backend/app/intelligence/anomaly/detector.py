import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from .features import anomaly_feature_vector, feature_matrix_for_customers

def fit_isolation_forest(db: Session):
    ids, X = feature_matrix_for_customers(db)
    if len(X)<5: return None, ids
    clf=IsolationForest(contamination=0.2, random_state=42)
    clf.fit(np.array(X))
    return clf, ids

def anomaly_score_isolation(db: Session, entity_type: str, entity_id: str) -> dict:
    # Optimized for large dataset: sample if >1000
    vec=np.array(anomaly_feature_vector(db, entity_type, entity_id)).reshape(1,-1)
    if entity_type=="CUSTOMER":
        try:
            ids, X = feature_matrix_for_customers(db)
            if len(X) > 1000:
                # sample 500 for stats to avoid 10k*queries
                import random
                idx = random.sample(range(len(X)), 500)
                X = [X[i] for i in idx]
                ids = [ids[i] for i in idx]
        except: X=[]
        if len(X)>=5:
            arr=np.array(X)
            means=arr.mean(axis=0)
            stds=arr.std(axis=0)+1e-6
            z=np.abs((vec[0]-means)/stds)
            z_max=float(z.max())
            # skip isolation forest for large dataset (heavy)
            if len(X) < 500:
                try:
                    clf,_=fit_isolation_forest(db)
                    if clf is not None:
                        iso = clf.decision_function(vec)[0]
                        isolation_score=float(1/(1+np.exp(iso)))
                    else: isolation_score=float(min(1, z_max/3))
                except: isolation_score=float(min(1, z_max/3))
            else:
                isolation_score=float(min(1, z_max/3))
            combined=max(z_max/3, isolation_score)
            is_anomaly= combined>0.7 or z_max>2.5
            return {"anomaly_score": round(float(combined),3),"z_max": round(z_max,2),"is_anomaly": bool(is_anomaly),"method":"isolation+ zscore" if len(X)<500 else "zscore-sampled"}
    # fallback simple threshold
    score=float(min(1, float(vec[0][0])/5 + float(vec[0][2])/2*0.2))
    return {"anomaly_score": round(score,3),"z_max": None,"is_anomaly": score>0.7,"method":"heuristic"}

def batch_anomaly(db: Session):
    ids, X = feature_matrix_for_customers(db)
    clf,_=fit_isolation_forest(db)
    arr=np.array(X) if len(X) else np.empty((0,8))
    scores=[]
    for i, vec in enumerate(arr):
        r=anomaly_score_isolation(db,"CUSTOMER", ids[i])
        scores.append({"entity_id": ids[i], **r})
    return scores
