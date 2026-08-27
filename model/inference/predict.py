import pathlib, pickle, sys
for p in [pathlib.Path(__file__).parents[2], pathlib.Path(__file__).parents[2] / "backend"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from model.features.schema import validate, FEATURE_SCHEMA
from model.config import ARTIFACTS

DEFAULT_ARTIFACT = ARTIFACTS / "fraud_model_v2.pkl"

def load_artifact(path=DEFAULT_ARTIFACT):
    if not path.exists():
        # fallback to legacy backend artifact
        alt = pathlib.Path(__file__).parents[3] / "backend" / "app" / "ml" / "models" / "fraud_baseline.pkl"
        if alt.exists():
            with open(alt, "rb") as f:
                model = pickle.load(f)
            return {"model": model, "feature_schema": FEATURE_SCHEMA, "threshold": 0.5, "version": "legacy"}
        raise FileNotFoundError(f"Artifact not found: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

def predict(features: dict, artifact_path=DEFAULT_ARTIFACT):
    validate(features)
    artifact = load_artifact(artifact_path) if isinstance(artifact_path, pathlib.Path) else load_artifact()
    model = artifact["model"]
    threshold = artifact.get("threshold", 0.5)
    version = artifact.get("version", "unknown")
    import numpy as np
    vec = np.array([features[k] for k in FEATURE_SCHEMA]).reshape(1, -1)
    prob = float(model.predict_proba(vec)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(vec)[0])
    prob = max(0.0, min(1.0, prob))
    pred = "HIGH_RISK" if prob >= threshold else "LOW_RISK"
    return {
        "fraud_probability": prob,
        "prediction": pred,
        "threshold": threshold,
        "model_version": version,
        "features_used": FEATURE_SCHEMA,
    }

def predict_from_db(db, entity_type: str, entity_id: str, artifact_path=DEFAULT_ARTIFACT):
    from model.features.builder import extract_features
    feats = extract_features(db, entity_type, entity_id)
    result = predict(feats, artifact_path=artifact_path)
    result["features"] = feats
    return result
