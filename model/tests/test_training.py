import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
from model.training.prepare import load_labeled_dataset
from model.training.split import stratified_split
from app.database import SessionLocal
import numpy as np
from model.features.schema import FEATURE_SCHEMA

def test_dataset():
    db=SessionLocal()
    data=load_labeled_dataset(db)
    assert len(data)==20
    assert sum(d["label"] for d in data)==8
    db.close()

def test_split():
    db=SessionLocal()
    from model.training.prepare import load_labeled_dataset
    data=load_labeled_dataset(db)
    X=np.array([[d["features"][k] for k in FEATURE_SCHEMA] for d in data])
    y=np.array([d["label"] for d in data])
    (Xtr,ytr),(Xva,yva),(Xte,yte)=stratified_split(X,y)
    assert len(ytr)==12 and len(yva)==4 and len(yte)==4
    db.close()
