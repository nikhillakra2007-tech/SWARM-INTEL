import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
from model.inference.predict import predict, load_artifact
from model.features.schema import FEATURE_SCHEMA

def test_artifact():
    art=load_artifact()
    assert "model" in art

def test_predict():
    feats={k:1.0 for k in FEATURE_SCHEMA}
    r=predict(feats)
    assert 0 <= r["fraud_probability"] <= 1
    assert r["prediction"] in ("HIGH_RISK","LOW_RISK")

def test_missing_feature():
    try:
        predict({"network_degree":1})
        assert False
    except ValueError:
        pass

def test_empty():
    try:
        predict({})
        assert False
    except ValueError:
        pass
