import sys, pathlib
for p in [pathlib.Path(__file__).parents[2], pathlib.Path(__file__).parents[2] / "backend"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from sqlalchemy import text
from sqlalchemy.orm import Session
from model.features.builder import extract_features

def load_labeled_dataset(db: Session):
    """
    Uses synthetic label: customer_status == 'SUSPECT' => fraud=1 else 0.
    Documented as SYNTHETIC/DEMO — not real fraud outcome.
    No leakage: features do not include future investigation outcome or risk_scores-derived high-risk counts beyond allowed schema.
    """
    rows = db.execute(text("SELECT customer_id, customer_status FROM customers ORDER BY customer_ref")).fetchall()
    data = []
    for cid, status in rows:
        feats = extract_features(db, "CUSTOMER", str(cid))
        label = 1 if status == "SUSPECT" else 0
        data.append({"entity_id": str(cid), "features": feats, "label": label, "status": status})
    return data

def dataframe_from_data(data):
    import pandas as pd
    from model.features.schema import FEATURE_SCHEMA
    rows = []
    for d in data:
        row = {k: d["features"][k] for k in FEATURE_SCHEMA}
        row["label"] = d["label"]
        row["entity_id"] = d["entity_id"]
        rows.append(row)
    return pd.DataFrame(rows)
