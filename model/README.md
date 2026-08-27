# Model — Fraud Probability (DEMO / SYNTHETIC)

**Purpose:** Learn patterns from lending features → predict `fraud_probability` (0-1) and `prediction` HIGH_RISK/LOW_RISK. Output is ML prediction only, not collective risk.

**Label:** Synthetic `customer_status == 'SUSPECT'` (8/20 = 40% fraud). Documented as demo; not real fraud.

**Features (7, deterministic order, leakage-checked):**
- `network_degree` — graph degree from entity_relationships
- `application_count`
- `device_count`
- `shared_device_count`
- `shared_bank_account_count`
- `applications_last_7d`
- `payment_delay_average`

Excluded leakage features: high_risk_neighbor_count, cluster_size, anomaly-derived scores, future alerts. Temporal split not used — dataset too small / no time-based onset; using stratified random (seed 42).

**Artifacts:** `model/artifacts/fraud_model_v1.pkl` (pickle pipeline + metadata) + `.json`. Also synced to `backend/app/ml/models/fraud_baseline.pkl` for backend inference.

**Training:** `python model/training/train_full.py` (loads 20 samples, 12/4/4 split, class_weight=balanced, StandardScaler+LogisticRegression vs RandomForest, threshold tuned 0.3-0.7 for best F1 with recall≥0.5). Final: LogisticRegression thr=0.3.

**Metrics (test, n=4, threshold 0.3):** precision 1.0, recall 1.0, f1 1.0, roc_auc 1.0, pr_auc 1.0, accuracy 1.0, confusion [[2,0],[0,2]]. Perfect due to tiny separable synthetic data — not production claim.

**Inference:** `from model.inference.predict import predict; predict({"network_degree":8, ...})` returns `{fraud_probability, prediction, threshold, model_version, features_used}`. Validates schema.

**Limitations:** 20 samples, single site synthetic, no temporal split, no cross-validation beyond single split.

**Backend:** `backend/app/services/ml_service.py` → `model.inference.predict.predict_from_db` via FastAPI `POST /api/predictions/{type}/{id}` and `POST /api/intelligence/analyze`.

Run `pytest model/tests -v` for tests.
