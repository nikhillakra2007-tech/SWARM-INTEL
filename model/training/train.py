import pathlib, pickle, json
from datetime import datetime, timezone
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from model.config import RANDOM_STATE

def train_baseline(X, y):
    # Logistic Regression with scaling + balanced weights
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(class_weight="balanced", max_iter=500, random_state=RANDOM_STATE))
    ])
    pipe.fit(X, y)
    return pipe

def train_rf(X, y):
    pipe = Pipeline([
        ("clf", RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=1))
    ])
    pipe.fit(X, y)
    return pipe

def train_gb(X, y):
    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(random_state=RANDOM_STATE)
    clf.fit(X, y)
    return clf

def save_artifact(model, feature_schema, threshold, metrics, version, path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": model,
        "feature_schema": feature_schema,
        "threshold": threshold,
        "metrics": metrics,
        "version": version,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "random_state": RANDOM_STATE,
    }
    with open(path, "wb") as f:
        pickle.dump(artifact, f)
    # also save json metadata without model
    meta = {k: v for k, v in artifact.items() if k != "model"}
    meta["feature_schema"] = feature_schema
    with open(path.with_suffix(".json"), "w") as jf:
        json.dump(meta, jf, indent=2, default=str)
    return path
