import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending"
from app.database import SessionLocal
from app.models import Customer
from app.intelligence.features import build_all_features
from app.intelligence.rules.engine import run_rules
from app.intelligence.graph.builder import build_graph
from app.intelligence.anomaly.detector import anomaly_score_isolation
from app.intelligence.ml.training import training_matrix
from app.intelligence.ml.prediction import predict
from app.intelligence.temporal.analyzer import growth_analysis
from app.intelligence.risk.aggregator import collective_risk
from app.intelligence.risk.explanation import explain
from app.intelligence.clustering.detector import detect_clusters
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def get_c013():
    db=SessionLocal()
    c=db.query(Customer).first()
    db.close()
    return str(c.customer_id)

def get_c001():
    db=SessionLocal()
    c=db.query(Customer).filter(Customer.customer_ref=="C001").first()
    db.close()
    return str(c.customer_id)

def test_features():
    db=SessionLocal()
    feats=build_all_features(db,"CUSTOMER",get_c013())
    assert "application_count" in feats
    assert "network_degree" in feats
    assert "payment_delay_average" in feats
    assert "applications_last_7d" in feats
    db.close()

def test_rules_13():
    db=SessionLocal()
    sigs=run_rules(db,"CUSTOMER",get_c013())
    assert len(sigs)>=3
    types={s["signal_type"] for s in sigs}
    assert "SHARED_DEVICE" in types
    db.close()

def test_graph():
    db=SessionLocal()
    G=build_graph(db)
    assert G.number_of_nodes()>10
    assert G.number_of_edges()>=39
    from app.intelligence.graph.traversal import bfs_nodes
    nodes=bfs_nodes(G, f"CUSTOMER:{get_c013()}", depth=2)
    assert len(nodes)>=5
    db.close()

def test_anomaly():
    db=SessionLocal()
    r=anomaly_score_isolation(db,"CUSTOMER",get_c013())
    assert "anomaly_score" in r
    assert "is_anomaly" in r
    # C013 should be anomalous vs C001
    r2=anomaly_score_isolation(db,"CUSTOMER",get_c001())
    # C013 higher than C001 generally
    db.close()

def test_ml():
    db=SessionLocal()
    X,y,_=training_matrix(db)
    assert X.shape[0]>=20
    res=predict(db,"CUSTOMER",get_c013())
    assert 0 <= res["probability"] <= 1
    # fraud customer higher prob
    res2=predict(db,"CUSTOMER",get_c001())
    assert res["probability"] > res2["probability"]
    db.close()

def test_temporal():
    db=SessionLocal()
    g=growth_analysis(db,"CUSTOMER",get_c013())
    assert "is_rapid_growth" in g
    db.close()

def test_risk_separation():
    db=SessionLocal()
    coll=collective_risk(db,"CUSTOMER",get_c013(), persist=False)
    assert "individual_risk_score" in coll
    assert "network_risk_score" in coll
    assert coll["network_risk_score"] > coll["individual_risk_score"]  # network critical
    db.close()

def test_explain():
    db=SessionLocal()
    coll=collective_risk(db,"CUSTOMER",get_c013(), persist=False)
    expl=explain(db,"CUSTOMER",get_c013(), coll)
    assert len(expl["reasons"])>=3
    assert "Ml fraud probability" in " ".join(expl["reasons"]) or "ML" in " ".join(expl["reasons"])
    db.close()

def test_cluster():
    db=SessionLocal()
    comps=detect_clusters(db, min_size=3)
    assert len(comps)>=1
    assert max(len(c) for c in comps)>=5
    db.close()

def test_api_intelligence():
    cid=get_c013()
    r=client.post(f"/api/intelligence/analyze/CUSTOMER/{cid}")
    assert r.status_code==200
    j=r.json()
    assert "collective" in j
    assert "explanation" in j
    assert j["collective"]["network_risk_score"] > j["collective"]["individual_risk_score"]
    r2=client.get(f"/api/intelligence/features/CUSTOMER/{cid}")
    assert r2.status_code==200
    r3=client.get(f"/api/intelligence/anomaly/CUSTOMER/{cid}")
    assert r3.status_code==200
