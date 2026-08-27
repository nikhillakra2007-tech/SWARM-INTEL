import pathlib, pickle
from app.config import get_settings
settings=get_settings()
MODEL_PATH=pathlib.Path(settings.MODEL_PATH)
# also fallback to app/ml/models

def load_model():
    for p in [MODEL_PATH, pathlib.Path("app/ml/models/fraud_baseline.pkl"), pathlib.Path(__file__).parents[3]/"app/ml/models/fraud_baseline.pkl"]:
        if p.exists():
            try:
                with open(p,"rb") as f: return pickle.load(f)
            except: continue
    return None

def model_exists(): return load_model() is not None
