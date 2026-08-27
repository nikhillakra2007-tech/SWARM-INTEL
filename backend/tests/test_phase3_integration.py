import os
os.environ["DATABASE_URL"]="postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending"
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from sqlalchemy import text
client=TestClient(app)

def get_id(ref, table="customers", col="customer_ref", idcol="customer_id"):
    from app.database import SessionLocal
    db=SessionLocal(); v=db.execute(text(f"SELECT {idcol} FROM {table} WHERE {col}=:r"), {"r": ref}).scalar(); db.close(); return str(v)

def test_suspicious_network():
    cid=get_id("C013")
    r=client.post(f"/api/intelligence/analyze/CUSTOMER/{cid}")
    assert r.status_code==200, r.text
    j=r.json()
    # individual vs network distinction is core
    assert j["individual_risk"]["score"] is not None
    assert j["network_risk"]["score"] is not None
    # suspicious network should be high
    assert j["network_risk"]["score"] > 60
    assert j["collective_risk"]["score"] > 70
    assert len(j["signals"]) >= 3
    assert j["ml_prediction"]["fraud_probability"] > 0.5

def test_normal_entity():
    cid=get_id("C001")
    r=client.post(f"/api/intelligence/analyze/CUSTOMER/{cid}")
    assert r.status_code==200
    j=r.json()
    assert j["collective_risk"]["score"] < 70  # normal lower

def test_invalid_id():
    r=client.post("/api/intelligence/analyze/CUSTOMER/31")
    assert r.status_code==400
    assert "Invalid UUID" in r.text or "Unsupported" in r.text

def test_unknown_entity():
    import uuid
    r=client.post(f"/api/intelligence/analyze/CUSTOMER/{uuid.uuid4()}")
    assert r.status_code==404

def test_missing_feature():
    from model.inference.predict import predict
    try:
        predict({})
        assert False
    except ValueError:
        pass

def test_missing_model():
    from model.inference.predict import load_artifact
    import pathlib
    try:
        load_artifact(pathlib.Path("/tmp/nonexistent.pkl"))
        assert False
    except FileNotFoundError:
        pass

def test_network_visualization_data():
    cid=get_id("C013")
    r=client.post(f"/api/intelligence/analyze/CUSTOMER/{cid}")
    j=r.json()
    assert "network" in j
    assert "degree" in j["network"] or "in_graph" in j["network"]
    assert "cluster" in j  # may be None or dict
    assert "evidence" in j
