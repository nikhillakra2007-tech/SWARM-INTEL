import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending"

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Customer, Device

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] in ("healthy","degraded")
    assert r.json()["database"] == "connected"

def test_list_customers():
    r = client.get("/api/customers?page=1&size=5")
    assert r.status_code == 200
    assert r.json()["total"] >= 20
    assert len(r.json()["items"]) == 5

def test_get_customer():
    db = SessionLocal()
    c = db.query(Customer).first()
    db.close()
    r = client.get(f"/api/customers/{c.customer_id}")
    assert r.status_code == 200
    assert r.json()["customer_ref"] == c.customer_ref

def test_network():
    db = SessionLocal()
    c = db.query(Customer).first()
    db.close()
    r = client.get(f"/api/relationships/CUSTOMER/{c.customer_id}")
    assert r.status_code == 200
    assert r.json()["count"] >= 5

def test_fraud_analyze():
    db = SessionLocal()
    c = db.query(Customer).first()
    db.close()
    r = client.post(f"/api/fraud/analyze/CUSTOMER/{c.customer_id}")
    assert r.status_code == 200
    assert r.json()["count"] >= 1

def test_risk():
    db = SessionLocal()
    c = db.query(Customer).first()
    db.close()
    # risk may need generation via analyze first
    r = client.get(f"/api/risk/CUSTOMER/{c.customer_id}")
    if r.status_code==404:
        r2=client.post(f"/api/intelligence/analyze/CUSTOMER/{c.customer_id}")
        r=client.get(f"/api/risk/CUSTOMER/{c.customer_id}")
    assert r.status_code == 200
    assert "latest" in r.json()

def test_clusters():
    r = client.get("/api/clusters")
    assert r.status_code == 200
    assert r.json()["total"] >= 2

def test_alerts():
    r = client.get("/api/alerts")
    assert r.status_code == 200
    assert r.json()["total"] >= 0

def test_graph_components():
    r = client.get("/api/network/components")
    assert r.status_code == 200
    assert r.json()["count"] >= 1
