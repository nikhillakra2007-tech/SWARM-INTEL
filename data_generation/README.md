# Data Generation — Synthetic Lending Ecosystem

> Synthetic data only — not real customers. For development/demo/testing.

**Purpose:** 50k-scale interconnected ecosystem for feature/graph/ML testing.

**Generate:** `python -m data_generation.generator` or `python model/training/train_full.py` after seeding.

**Seed DB:** `python -m data_generation.seed.seed_database --reset` (requires explicit --reset, validates first). Without --reset, inserts ON CONFLICT DO NOTHING.

**Validate:** `from data_generation.validation.validator import validate, report`

**Seed:** Config `SEED=42` reproducible. Distributions: 85% normal, 10% suspicious, 5% fraud (labels from scenario, not leaked as feature). Scenarios 10 types: shared device/bank/guarantor, dealer-centric, burst, identity, IP, location, mixed, emerging (+5 deterministic DEMO_FRAUD_001-005).

**Temporal:** 180 days 2025-03-01 to 2025-08-31, bursts coordinated, emerging grows over 10 days.

**Relationships:** 60k entity_relationships (SHARED_DEVICE etc) + clusters.

**Ground truth:** `eco.ground_truth` maps customer_id→label, not used as ML feature.

**Commands:**
```
python -m data_generation.seed.seed_database --reset
python -m model.training.train_full
pytest data_generation/tests -v
```

**No real PII:** All hashes synthetic.
