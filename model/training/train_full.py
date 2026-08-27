"""
Full training pipeline: load → split → train LR + RF → evaluate → choose → save
Run from project root: python -m model.training.train_full
Or: python model/training/train_full.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
import numpy as np
from sqlalchemy import text
from app.database import SessionLocal
from model.training.prepare import load_labeled_dataset
from model.training.split import stratified_split, time_aware_split_note
from model.training.train import train_baseline, train_rf, save_artifact
from model.training.evaluate import evaluate, choose_threshold
from model.config import ARTIFACTS, MODEL_VERSION
from model.features.schema import FEATURE_SCHEMA as SCHEMA

def main():
    db = SessionLocal()
    try:
        data = load_labeled_dataset(db)
        total = len(data)
        fraud = sum(1 for d in data if d["label"]==1)
        print(f"Loaded {total} samples: fraud={fraud} non-fraud={total-fraud} ({fraud/total*100:.1f}%)")
        if total < 10:
            print("Not enough data for meaningful ML")
        X = np.array([[d["features"][k] for k in SCHEMA] for d in data])
        y = np.array([d["label"] for d in data])
        (X_train, y_train), (X_val, y_val), (X_test, y_test) = stratified_split(X, y)
        print(f"Split: train={len(y_train)} val={len(y_val)} test={len(y_test)}")
        print(time_aware_split_note())
        # Train candidates
        lr = train_baseline(X_train, y_train)
        rf = train_rf(X_train, y_train)
        # Evaluate on val for threshold tuning
        for name, model in [("LogisticRegression", lr), ("RandomForest", rf)]:
            y_prob = model.predict_proba(X_val)[:,1]
            thr = choose_threshold(y_val, y_prob)
            m = evaluate(y_val, y_prob, threshold=thr)
            print(f"{name} val: prec={m['precision']:.3f} rec={m['recall']:.3f} f1={m['f1']:.3f} roc={m['roc_auc']} thr={thr} cm={m['confusion_matrix']}")
        # Choose final: higher F1 on val
        def f1_for(model):
            prob = model.predict_proba(X_val)[:,1]
            return evaluate(y_val, prob, threshold=choose_threshold(y_val, prob))["f1"]
        final = lr if f1_for(lr) >= f1_for(rf) else rf
        final_name = "LogisticRegression" if final is lr else "RandomForest"
        # Final threshold from val
        val_prob = final.predict_proba(X_val)[:,1]
        thr = choose_threshold(y_val, val_prob)
        # Evaluate on test with chosen threshold
        test_prob = final.predict_proba(X_test)[:,1]
        test_metrics = evaluate(y_test, test_prob, threshold=thr)
        print(f"Final: {final_name} thr={thr} test prec={test_metrics['precision']:.3f} rec={test_metrics['recall']:.3f} f1={test_metrics['f1']:.3f} roc={test_metrics['roc_auc']} pr={test_metrics['pr_auc']} acc={test_metrics['accuracy']:.3f}")
        print(f"Confusion matrix test: {test_metrics['confusion_matrix']}")
        # Feature importance
        if hasattr(final, "named_steps"):
            # pipeline
            clf = final.named_steps.get("clf", final)
        else:
            clf = final
        if hasattr(clf, "coef_"):
            imp = {k: float(v) for k, v in zip(SCHEMA, clf.coef_[0])}
            print("Coefficients:", imp)
        elif hasattr(clf, "feature_importances_"):
            imp = {k: float(v) for k, v in zip(SCHEMA, clf.feature_importances_)}
            print("Importances:", imp)
        # Save artifact
        artifact_path = ARTIFACTS / f"{MODEL_VERSION}.pkl"
        save_artifact(final, SCHEMA, thr, test_metrics, MODEL_VERSION, artifact_path)
        # Also ensure standard name
        import shutil
        std = ARTIFACTS / "fraud_model_v1.pkl"
        if artifact_path.resolve() != std.resolve():
            shutil.copy(artifact_path, std)
        print(f"Saved to {artifact_path} and fraud_model_v1.pkl")
        print(f"Features: {SCHEMA}")
        print("DEMO/SYNTHETIC MODEL — not validated on real fraud")
        return test_metrics
    finally:
        db.close()

if __name__ == "__main__":
    main()
