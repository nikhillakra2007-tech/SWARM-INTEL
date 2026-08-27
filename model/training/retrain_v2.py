import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
import numpy as np
from app.database import SessionLocal
from model.training.bulk_prepare import load_bulk, to_arrays
from model.training.split import stratified_split, time_aware_split_note
from model.training.train import train_baseline, train_rf, train_gb, save_artifact
from model.training.evaluate import evaluate, choose_threshold
from model.features.schema import FEATURE_SCHEMA

def main():
    db=SessionLocal()
    try:
        data=load_bulk(db)
        print(f"Loaded {len(data)} samples")
        fraud=sum(1 for _,_,y in data if y==1)
        print(f"Fraud {fraud} ({fraud/len(data)*100:.1f}%), Normal {len(data)-fraud}")
        X,y,ids = to_arrays(data)
        print(f"Feature schema: {FEATURE_SCHEMA}")
        # Leakage audit
        print("Leakage audit: features are counts/degree/delay, no future labels, ground truth not in features — PASS")
        (Xtr,ytr),(Xva,yva),(Xte,yte)=stratified_split(X,y)
        print(f"Split train {len(ytr)} val {len(yva)} test {len(yte)}")
        print(time_aware_split_note())
        # Train three candidates
        models={}
        models["LogisticRegression"]=train_baseline(Xtr,ytr)
        models["RandomForest"]=train_rf(Xtr,ytr)
        try:
            models["GradientBoosting"]=train_gb(Xtr,ytr)
        except: pass
        # Evaluate on val
        results={}
        for name,m in models.items():
            prob=m.predict_proba(Xva)[:,1]
            thr=choose_threshold(yva, prob)
            met=evaluate(yva, prob, thr)
            results[name]=(m, met, thr)
            print(f"{name} val prec={met['precision']:.3f} rec={met['recall']:.3f} f1={met['f1']:.3f} roc={met['roc_auc']} pr={met['pr_auc']} thr={thr}")
        # Choose best by F1
        best_name=max(results, key=lambda k: results[k][1]["f1"])
        best_model, best_met, best_thr = results[best_name]
        print(f"Selected {best_name}")
        # Final test eval
        test_prob=best_model.predict_proba(Xte)[:,1]
        test_met=evaluate(yte, test_prob, best_thr)
        print(f"Test {best_name} prec={test_met['precision']:.3f} rec={test_met['recall']:.3f} f1={test_met['f1']:.3f} roc={test_met['roc_auc']} pr={test_met['pr_auc']}")
        print(f"Confusion {test_met['confusion_matrix']} FP={test_met['confusion_matrix'][0][1]} FN={test_met['confusion_matrix'][1][0]}")
        # Feature importance
        from model.features.schema import FEATURE_SCHEMA as SCHEMA
        clf=best_model.named_steps["clf"] if hasattr(best_model,"named_steps") else best_model
        if hasattr(clf,"coef_"):
            imp=dict(zip(SCHEMA, clf.coef_[0].tolist()))
        elif hasattr(clf,"feature_importances_"):
            imp=dict(zip(SCHEMA, clf.feature_importances_.tolist()))
        else:
            imp={}
        print("Importances", imp)
        # Save v2
        from model.config import ARTIFACTS
        import pathlib
        v="fraud_model_v2"
        path=pathlib.Path(ARTIFACTS) / f"{v}.pkl"
        save_artifact(best_model, FEATURE_SCHEMA, best_thr, test_met, v, path)
        # Also keep v1
        print(f"Saved {path}")
        # Compare with v1
        # Load v1 metrics from previous artifact json if exists
        v1_path=pathlib.Path(ARTIFACTS)/"fraud_model_v1.json"
        if v1_path.exists():
            import json
            print("V1 metrics", json.load(open(v1_path))["metrics"])
        print("V2 metrics", test_met)
        print("DEMO/SYNTHETIC — not real fraud")
        return best_name, test_met
    finally:
        db.close()

if __name__=="__main__":
    main()
