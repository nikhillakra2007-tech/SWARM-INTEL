# Swarm Intelligence Lending Network — Architecture

## Pipeline

```
RAW LENDING DATA (customers, applications, loans, payments)
        ↓
ENTITY RELATIONSHIPS (shared device/mobile/bank/address/guarantor/ip/dealer links)
        ↓
BEHAVIOURAL EVENTS (application_events — login, device_changed, etc.)
        ↓
FRAUD SIGNALS (fraud_signals — per-entity indicators)
        ↓
NETWORK / CLUSTER DETECTION (fraud_clusters + fraud_cluster_members)
        ↓
RISK SCORING (risk_scores — append-only history per entity)
        ↓
AI PREDICTIONS (model_versions + predictions — versioned)
        ↓
ALERTS (fraud_alerts — actionable, linked to cluster)
        ↓
INVESTIGATION (investigations + investigation_actions — audit trail)
        ↓
AUDIT / GOVERNANCE (audit_logs)
```

## Design decisions

### 1. 31-table core
Groups:
- G1 Identity: `customers`, `mobile_numbers`, `customer_mobile_links`, `addresses`, `customer_address_links` (5)
- G2 Financial: `bank_accounts`, `customer_bank_links` (2)
- G3 Device/IP: `devices`, `customer_device_links`, `ip_addresses` (3)
- G4 Dealer: `dealers`, `dealer_customer_links` (2)
- G5 Lending: `loan_applications`, `loans` (2)
- G6 Guarantor: `guarantors`, `loan_guarantors` (2)
- G7 Payments: `payments`, `repayment_behaviour` (2)
- G8 Location/Activity: `locations`, `application_events` (2)
- G9 Swarm network: `entity_relationships` (1) — **core**
- G10 Fraud intelligence: `fraud_signals`, `risk_scores` (2)
- G11 Clusters: `fraud_clusters`, `fraud_cluster_members` (2)
- G12 Alerts: `fraud_alerts` (1)
- G13 Investigation: `investigations`, `investigation_actions` (2)
- G14 AI/ML: `model_versions`, `predictions` (2)
- G15 Governance: `audit_logs` (1)

Total = 31.

### 2. Polymorphic intelligence tables
`entity_relationships`, `fraud_signals`, `risk_scores`, `fraud_cluster_members`, `predictions`, `fraud_alerts` use `(entity_type VARCHAR, entity_id UUID)` without hard FKs. CHECK constrains `entity_type`; application layer verifies `entity_id` exists in the implied table. See `schema/004_relationships.sql`.

### 3. Preservation
- `ON DELETE RESTRICT` for financial/identity parents — history is never cascade-deleted.
- `risk_scores`, `predictions`, `fraud_signals`, `audit_logs`, `investigation_actions` are append-only.
- `repayment_behaviour` keeps derived features separate from raw `payments`.

### 4. Security
- PAN/Aadhaar/mobile/bank/IP stored as SHA-256 hashes/tokens.
- `audit_logs` stores old/new as JSONB without sensitive plaintext.
- No credentials in repo; `../.env.example` documents env vars.

### 5. Indexes
Bidirectional indexes on `entity_relationships(source)` and `(target)` enable O(log n) graph traversal both ways. Additional composite indexes on `(entity_type, entity_id)` for intelligence tables; `(customer_id, event_timestamp)` and `(device_id, event_timestamp)` for behavioural queries.

### 6. Views
- `customer_risk_overview` — latest risk + counts per customer
- `active_fraud_alerts` — unresolved alerts + cluster
- `fraud_cluster_overview` — cluster + active member/open alert counts
- `customer_network_connections` — union of outgoing/incoming edges
- `dealer_risk_overview` — dealer exposure + avg/max risk
- `device_customer_network` — device → customer fan-out + high-risk flag

### 7. Supabase migration
Schema uses only standard PostgreSQL (pgcrypto, uuid-ossp). Supabase PostgreSQL requires no changes; optionally enable `pg_trgm` for fuzzy matching. Run files in numeric order; seeds are plain INSERTs.

## Folder

```
database/
  schema/   001_extensions .. 007_views
  seeds/    001_reference_data .. 005_fraud_scenarios
  queries/  fraud_network_queries + risk/cluster/investigation
  docs/     architecture, ERD, data_dictionary
  scripts/  setup/reset/seed + generate_seeds.py
```
