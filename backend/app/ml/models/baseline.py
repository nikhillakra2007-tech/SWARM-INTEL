import os, pickle, pathlib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = pathlib.Path(__file__).parent / "fraud_baseline.pkl"

def train_baseline(X, y):
    # Prefer RF if enough data else LogisticRegression
    if len(X) < 10:
        clf = LogisticRegression()
    else:
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    return clf

def load_model():
    if MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None

def predict_proba(model, features_vector):
    if model is None:
        return 0.5
    arr = np.array(features_vector).reshape(1, -1)
    try:
        return float(model.predict_proba(arr)[0][1])
    except Exception:
        return 0.5
