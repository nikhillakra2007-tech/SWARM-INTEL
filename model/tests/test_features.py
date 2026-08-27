import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
from model.features.schema import FEATURE_SCHEMA, validate
from model.features.builder import extract_features
from app.database import SessionLocal

def test_schema_order():
    assert FEATURE_SCHEMA == ["network_degree","application_count","device_count","shared_device_count","shared_bank_account_count","applications_last_7d","payment_delay_average"]

def test_validate_missing():
    try:
        validate({"network_degree":1})
        assert False, "should raise"
    except ValueError:
        pass

def test_extract():
    db=SessionLocal()
    try:
        feats=extract_features(db,"CUSTOMER", str(__import__("sqlalchemy").text("dummy")))
    except: pass
    db=SessionLocal()
    from sqlalchemy import text
    cid=str(db.execute(text("SELECT customer_id FROM customers LIMIT 1")).scalar())
    feats=extract_features(db,"CUSTOMER", cid)
    assert set(feats.keys())==set(FEATURE_SCHEMA)
    assert all(isinstance(v,float) for v in feats.values())
    db.close()
