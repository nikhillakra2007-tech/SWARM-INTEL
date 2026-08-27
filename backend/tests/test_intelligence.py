import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending"

from app.database import SessionLocal
from app.models import Customer
from app.intelligence.graph.engine import build_graph, neighbors
from app.fraud.signals.engine import analyze_entity
from app.ml.features.engine import build_features

def test_graph_build():
    db = SessionLocal()
    G = build_graph(db)
    assert G.number_of_nodes() > 0
    assert G.number_of_edges() >= 39
    db.close()

def test_fraud_cluster_reconstruction():
    db = SessionLocal()
    c = db.query(Customer).first()
    signals = analyze_entity(db, "CUSTOMER", str(c.customer_id))
    types = {s["signal_type"] for s in signals}
    assert "SHARED_DEVICE" in types
    assert "SHARED_MOBILE" in types
    db.close()

def test_features():
    db = SessionLocal()
    c = db.query(Customer).first()
    feats = build_features(db, "CUSTOMER", str(c.customer_id))
    assert feats["shared_device_count"] >= 1
    assert feats["degree"] >= 4
    db.close()
