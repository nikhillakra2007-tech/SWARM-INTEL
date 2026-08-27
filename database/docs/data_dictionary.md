# Data Dictionary — Swarm Intelligence Lending Network

> All hashes are SHA-256 hex. No plaintext PII is stored.

## 1 customers

| Column | Type | Nullable | Default | Sensitive | Meaning | Example |
|--------|------|----------|---------|-----------|---------|---------|
| customer_id | UUID | No | gen_random_uuid() | No | PK | `c26abb...` |
| customer_ref | VARCHAR(20) | No | — | No | Human code, unique | `C013` |
| full_name | VARCHAR(200) | No | — | No | Display name (synthetic) | `Imran Khan` |
| date_of_birth | DATE | Yes | — | No | DOB | `1993-03-08` |
| gender | gender ENUM | Yes | — | No | Gender | `MALE` |
| pan_hash | VARCHAR(128) | Yes | — | Yes (hash) | SHA-256 of PAN | `a3f...` |
| aadhaar_hash | VARCHAR(128) | Yes | — | Yes (hash) | SHA-256 of Aadhaar | `9c2...` |
| occupation | VARCHAR(100) | Yes | — | No | Occupation | `DRIVER` |
| income_band | income_band | No | UNKNOWN | No | Band | `LOW` |
| customer_status | customer_status | No | ACTIVE | No | ACTIVE/SUSPECT/BLOCKED... | `SUSPECT` |
| created_at | TIMESTAMPTZ | No | now() | No | Created | `2026-08-01...` |
| updated_at | TIMESTAMPTZ | No | now() | No | Updated (auto) | `...` |

## 2 mobile_numbers

| Column | Type | Nullable | Default | Sensitive | Meaning | Example |
|--------|------|----------|---------|-----------|---------|---------|
| mobile_id | UUID | No | gen_random_uuid() | No | PK | `...` |
| mobile_hash | VARCHAR(128) | No | — | Yes | SHA-256 of number | `e7b...` |
| country_code | VARCHAR(5) | No | +91 | No | ISD | `+91` |
| mobile_status | mobile_status | No | ACTIVE | No | Status | `SUSPECT` |
| first_seen | TIMESTAMPTZ | No | now() | No | First observed | `2025-01-15...` |
| last_seen | TIMESTAMPTZ | No | now() | No | Last observed | `2026-08-20...` |
| created_at | TIMESTAMPTZ | No | now() | No | — | — |

## 3 customer_mobile_links

| Column | Type | Nullable | Default | Meaning |
|--------|------|----------|---------|---------|
| link_id | UUID | No | gen_random_uuid() | PK |
| customer_id | UUID | No | — | FK → customers |
| mobile_id | UUID | No | — | FK → mobile_numbers |
| relationship_type | VARCHAR(30) | No | PRIMARY | PRIMARY/SECONDARY/ALTERNATE... |
| is_primary | BOOLEAN | No | false | Primary flag |
| first_seen | TIMESTAMPTZ | No | now() | — |
| last_seen | TIMESTAMPTZ | No | now() | — |
| created_at | TIMESTAMPTZ | No | now() | — |
| UNIQUE | (customer_id, mobile_id) | — | — | One link per pair |

## 4 addresses

| Column | Type | Nullable | Default | Meaning | Example |
|--------|------|----------|---------|---------|---------|
| address_id | UUID | No | gen_random_uuid() | PK | `...` |
| address_hash | VARCHAR(128) | No | — | SHA-256 of text | `f1a...` |
| address_text | VARCHAR(500) | Yes | — | Street text | `Dharavi Shared Chawl...` |
| city | VARCHAR(100) | Yes | — | City | `Mumbai` |
| district | VARCHAR(100) | Yes | — | District | `Mumbai` |
| state | VARCHAR(100) | Yes | — | State | `Maharashtra` |
| pincode | VARCHAR(10) | Yes | — | 6-digit | `400017` |
| latitude | NUMERIC(9,6) | Yes | — | Lat | `19.042` |
| longitude | NUMERIC(9,6) | Yes | — | Lon | `72.856` |
| created_at | TIMESTAMPTZ | No | now() | — | — |

## 5 customer_address_links — (customer_id FK, address_id FK, relationship_type RESIDENTIAL/PERMANENT/OFFICE..., is_primary, timestamps) UNIQUE(customer_id, address_id, relationship_type)

## 6 bank_accounts

| Column | Type | Nullable | Default | Sensitive | Meaning | Example |
|--------|------|----------|---------|-----------|---------|---------|
| bank_account_id | UUID | No | gen_random_uuid() | No | PK | `...` |
| account_hash | VARCHAR(128) | No | — | Yes | SHA-256 | `b8c...` |
| bank_name | VARCHAR(150) | No | — | No | Bank | `State Bank of India` |
| ifsc | VARCHAR(11) | Yes | — | No | IFSC | `SBIN0000007` |
| account_type | bank_account_type | No | SAVINGS | No | Type | `SAVINGS` |
| account_status | bank_account_status | No | ACTIVE | No | Status | `SUSPECT` |
| first_seen | TIMESTAMPTZ | No | now() | No | — | — |
| last_seen | TIMESTAMPTZ | No | now() | No | — | — |
| created_at | TIMESTAMPTZ | No | now() | No | — | — |

## 7 customer_bank_links — (customer_id FK, bank_account_id FK, relationship_type PRIMARY/SECONDARY/SALARY/JOINT, is_primary, timestamps) UNIQUE(customer_id, bank_account_id)

## 8 devices

| Column | Type | Nullable | Default | Meaning | Example |
|--------|------|----------|---------|---------|---------|
| device_id | UUID | No | gen_random_uuid() | PK | `...` |
| device_fingerprint | VARCHAR(256) | No | — | Unique fingerprint | `fp_shared_device_FRAUD_X1` |
| device_type | device_type | No | MOBILE | MOBILE/DESKTOP/TABLET... | `MOBILE` |
| os | VARCHAR(100) | Yes | — | OS | `Android 13` |
| browser | VARCHAR(100) | Yes | — | Browser | `Chrome` |
| manufacturer | VARCHAR(100) | Yes | — | Make | `Xiaomi` |
| model | VARCHAR(100) | Yes | — | Model | `Redmi Note 12` |
| first_seen | TIMESTAMPTZ | No | now() | — | — |
| last_seen | TIMESTAMPTZ | No | now() | — | — |
| device_status | device_status | No | ACTIVE | Status | `SUSPECT` |
| created_at | TIMESTAMPTZ | No | now() | — | — |

## 9 customer_device_links — (customer_id FK, device_id FK, timestamps) UNIQUE(customer_id, device_id)

## 10 ip_addresses — ip_id PK, ip_hash UNIQUE (hashed), ip_version V4/V6, first_seen, last_seen, created_at

## 11 dealers — dealer_id PK, dealer_code UNIQUE DL..., dealer_name, dealer_type DSA/BRANCH/ONLINE..., address_id FK→addresses, dealer_status, onboarding_date, created_at, updated_at

## 12 dealer_customer_links — dealer_id FK, customer_id FK, first/last_application_at, application_count, relationship_status, timestamps UNIQUE(dealer_id, customer_id)

## 13 loan_applications — application_id PK, application_ref UNIQUE APP..., customer_id FK, dealer_id FK, requested_amount NUMERIC(12,2), tenure_months, application_timestamp, application_status, decision, risk_score 0-100, fraud_score 0-100, timestamps

## 14 loans — loan_id PK, application_id UNIQUE FK, loan_account_ref UNIQUE LN..., sanctioned_amount, disbursed_amount (≤ sanctioned), interest_rate, tenure_months, disbursement_date, loan_status, timestamps

## 15 guarantors — guarantor_id PK, guarantor_ref UNIQUE G..., full_name, identity_hash, mobile_id FK, address_id FK, created_at

## 16 loan_guarantors — application_id FK, guarantor_id FK, relationship_type GUARANTOR/CO_APPLICANT/REFERENCE, created_at UNIQUE(application_id, guarantor_id)

## 17 payments — payment_id PK, loan_id FK, payment_date, amount, payment_method, payment_status, days_past_due, transaction_ref, transaction_hash (hash), created_at

## 18 repayment_behaviour — behaviour_id PK, loan_id FK, avg_payment_delay_days, missed/early/partial/bounce counts, payment_velocity, behaviour_score 0-100, calculated_at, created_at UNIQUE(loan_id, calculated_at) — derived, does not replace payments

## 19 locations — location_id PK, latitude, longitude, city, district, state, pincode, created_at

## 20 application_events — event_id PK, application_id FK, customer_id FK, device_id FK, ip_id FK, location_id FK, event_type (APPLICATION_STARTED/SUBMITTED/LOGIN/DEVICE_CHANGED...), event_timestamp, metadata JSONB, created_at — event_type CHECK list is extensible; add values via migration

## 21 entity_relationships — relationship_id PK, source_entity_type VARCHAR CHECK, source_entity_id UUID, target_entity_type VARCHAR CHECK, target_entity_id UUID, relationship_type (SHARED_DEVICE/SHARED_MOBILE/SHARED_BANK_ACCOUNT/SHARED_ADDRESS/SHARED_GUARANTOR/SAME_IP/SAME_DEALER/SIMILAR_BEHAVIOUR/SUSPICIOUS_LINK...), strength 0-1, confidence 0-1, evidence_count, first_seen, last_seen, metadata JSONB, timestamps UNIQUE(source, target, type) CHECK no self-ref — **polymorphic, no hard FK** — see architecture

## 22 fraud_signals — signal_id PK, entity_type VARCHAR CHECK, entity_id UUID (polymorphic), signal_type CHECK, severity LOW/MEDIUM/HIGH/CRITICAL, score 0-100, confidence 0-1, description, detected_at, expires_at (nullable), evidence JSONB, created_at

## 23 risk_scores — risk_score_id PK, entity_type VARCHAR CHECK, entity_id UUID (polymorphic), risk_score 0-100, fraud_probability 0-1, risk_level LOW/MEDIUM/HIGH/CRITICAL, model_version, calculated_at, feature_snapshot JSONB, created_at — append-only history

## 24 fraud_clusters — cluster_id PK, cluster_ref UNIQUE F-..., cluster_type, risk_score 0-100, member_count, cluster_status ACTIVE/UNDER_REVIEW/CONFIRMED_FRAUD..., detected_at, last_updated_at, metadata JSONB

## 25 fraud_cluster_members — member_id PK, cluster_id FK CASCADE, entity_type VARCHAR CHECK, entity_id UUID (polymorphic), membership_score 0-1, joined_at, left_at nullable, UNIQUE(cluster_id, entity_type, entity_id) — supports Customers/Devices/Mobiles/BankAccounts/Dealers/Addresses/Guarantors/IPs

## 26 fraud_alerts — alert_id PK, alert_ref UNIQUE ALT-..., entity_type VARCHAR nullable CHECK, entity_id UUID nullable (polymorphic), cluster_id FK nullable, alert_type CHECK, severity, risk_score, alert_status OPEN/ACKNOWLEDGED/IN_INVESTIGATION/RESOLVED..., generated_at, resolved_at nullable, evidence JSONB, created_at

## 27 investigations — investigation_id PK, alert_id FK RESTRICT, investigator_ref, investigation_status OPEN/IN_PROGRESS/ON_HOLD/CLOSED..., priority LOW/MEDIUM/HIGH/URGENT, notes, opened_at, closed_at nullable, timestamps

## 28 investigation_actions — action_id PK, investigation_id FK CASCADE, action_type CHECK (NOTE_ADDED/STATUS_CHANGED/EVIDENCE_ADDED/ASSIGNED...), performed_by, notes, performed_at, created_at — audit trail

## 29 model_versions — model_id PK, model_name, version, model_type FRAUD_CLASSIFIER/RISK_SCORER..., training_completed_at, performance_metrics JSONB, model_status TRAINING/ACTIVE/RETIRED..., created_at UNIQUE(model_name, version)

## 30 predictions — prediction_id PK, model_id FK RESTRICT, entity_type VARCHAR CHECK, entity_id UUID (polymorphic), prediction_type, prediction_score 0-1, prediction_label, feature_snapshot JSONB, predicted_at, created_at — linked to model_version

## 31 audit_logs — audit_id PK, user_ref, action CHECK (CREATE/UPDATE/DELETE/VIEW...), entity_type VARCHAR nullable, entity_id UUID nullable (polymorphic), old_value JSONB, new_value JSONB, created_at

## Sensitive summary

- Hashes/tokens (not plaintext): pan_hash, aadhaar_hash, mobile_hash, account_hash, transaction_hash, ip_hash, identity_hash, address_hash.
- Plaintext location/bank/device metadata is non-identifying demo data.
- Audit logs store JSONB diffs; do not log raw PII.
