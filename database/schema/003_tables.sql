-- =============================================================================
-- 003_tables.sql — 31 core tables for Swarm Intelligence Lending Network
-- =============================================================================
-- Order respects FK dependencies. Polymorphic intelligence tables
-- (entity_relationships, fraud_signals, risk_scores, etc.) use
-- (entity_type VARCHAR, entity_id UUID) without hard FKs — see 004.
-- All monetary columns use NUMERIC(12,2). Timestamps default to now().
-- Sensitive identifiers are stored as hashes/tokens, never plaintext.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- GROUP 1 — CUSTOMER / IDENTITY  (Tables 1-5)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS customers (
    customer_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_ref        VARCHAR(20)  NOT NULL UNIQUE,
    full_name           VARCHAR(200) NOT NULL,
    date_of_birth       DATE,
    gender              gender,
    pan_hash            VARCHAR(128),
    aadhaar_hash        VARCHAR(128),
    occupation          VARCHAR(100),
    income_band         income_band NOT NULL DEFAULT 'UNKNOWN',
    customer_status     customer_status NOT NULL DEFAULT 'ACTIVE',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_customer_ref_format CHECK (customer_ref ~ '^C[0-9]{3,}$'),
    CONSTRAINT chk_pan_hash_len CHECK (pan_hash IS NULL OR char_length(pan_hash) >= 32),
    CONSTRAINT chk_aadhaar_hash_len CHECK (aadhaar_hash IS NULL OR char_length(aadhaar_hash) >= 32)
);

CREATE TABLE IF NOT EXISTS mobile_numbers (
    mobile_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mobile_hash         VARCHAR(128) NOT NULL UNIQUE,
    country_code        VARCHAR(5)   NOT NULL DEFAULT '+91',
    mobile_status       mobile_status NOT NULL DEFAULT 'ACTIVE',
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_mobile_hash_len CHECK (char_length(mobile_hash) >= 32)
);

CREATE TABLE IF NOT EXISTS customer_mobile_links (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    mobile_id           UUID NOT NULL REFERENCES mobile_numbers(mobile_id) ON DELETE RESTRICT,
    relationship_type   VARCHAR(30) NOT NULL DEFAULT 'PRIMARY' CHECK (relationship_type IN ('PRIMARY','SECONDARY','ALTERNATE','EMERGENCY','UNKNOWN')),
    is_primary          BOOLEAN NOT NULL DEFAULT false,
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (customer_id, mobile_id)
);

CREATE TABLE IF NOT EXISTS addresses (
    address_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    address_hash        VARCHAR(128) NOT NULL UNIQUE,
    address_text        VARCHAR(500),
    city                VARCHAR(100),
    district            VARCHAR(100),
    state               VARCHAR(100),
    pincode             VARCHAR(10),
    latitude            NUMERIC(9,6),
    longitude           NUMERIC(9,6),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_pincode_format CHECK (pincode IS NULL OR pincode ~ '^[0-9]{6}$'),
    CONSTRAINT chk_lat CHECK (latitude IS NULL OR (latitude BETWEEN -90 AND 90)),
    CONSTRAINT chk_lon CHECK (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
);

CREATE TABLE IF NOT EXISTS customer_address_links (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    address_id          UUID NOT NULL REFERENCES addresses(address_id) ON DELETE RESTRICT,
    relationship_type   VARCHAR(30) NOT NULL DEFAULT 'RESIDENTIAL' CHECK (relationship_type IN ('RESIDENTIAL','PERMANENT','OFFICE','CORRESPONDENCE','OTHER')),
    is_primary          BOOLEAN NOT NULL DEFAULT false,
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (customer_id, address_id, relationship_type)
);

-- ---------------------------------------------------------------------------
-- GROUP 2 — FINANCIAL ENTITIES  (Tables 6-7)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bank_accounts (
    bank_account_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_hash        VARCHAR(128) NOT NULL UNIQUE,
    bank_name           VARCHAR(150) NOT NULL,
    ifsc                VARCHAR(11),
    account_type        bank_account_type NOT NULL DEFAULT 'SAVINGS',
    account_status      bank_account_status NOT NULL DEFAULT 'ACTIVE',
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_ifsc_format CHECK (ifsc IS NULL OR ifsc ~ '^[A-Z]{4}0[A-Z0-9]{6}$'),
    CONSTRAINT chk_account_hash_len CHECK (char_length(account_hash) >= 32)
);

CREATE TABLE IF NOT EXISTS customer_bank_links (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    bank_account_id     UUID NOT NULL REFERENCES bank_accounts(bank_account_id) ON DELETE RESTRICT,
    relationship_type   VARCHAR(30) NOT NULL DEFAULT 'PRIMARY' CHECK (relationship_type IN ('PRIMARY','SECONDARY','SALARY','JOINT','UNKNOWN')),
    is_primary          BOOLEAN NOT NULL DEFAULT false,
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (customer_id, bank_account_id)
);

-- ---------------------------------------------------------------------------
-- GROUP 3 — DEVICE INTELLIGENCE  (Tables 8-10)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS devices (
    device_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_fingerprint  VARCHAR(256) NOT NULL UNIQUE,
    device_type         device_type NOT NULL DEFAULT 'MOBILE',
    os                  VARCHAR(100),
    browser             VARCHAR(100),
    manufacturer        VARCHAR(100),
    model               VARCHAR(100),
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    device_status       device_status NOT NULL DEFAULT 'ACTIVE',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS customer_device_links (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    device_id           UUID NOT NULL REFERENCES devices(device_id) ON DELETE RESTRICT,
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (customer_id, device_id)
);

CREATE TABLE IF NOT EXISTS ip_addresses (
    ip_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip_hash             VARCHAR(128) NOT NULL UNIQUE,
    ip_version          ip_version NOT NULL DEFAULT 'V4',
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_ip_hash_len CHECK (char_length(ip_hash) >= 16)
);

-- ---------------------------------------------------------------------------
-- GROUP 4 — DEALER NETWORK  (Tables 11-12)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dealers (
    dealer_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dealer_code         VARCHAR(20)  NOT NULL UNIQUE,
    dealer_name         VARCHAR(200) NOT NULL,
    dealer_type         dealer_type  NOT NULL DEFAULT 'DSA',
    address_id          UUID REFERENCES addresses(address_id) ON DELETE SET NULL,
    dealer_status       dealer_status NOT NULL DEFAULT 'ACTIVE',
    onboarding_date     DATE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_dealer_code_format CHECK (dealer_code ~ '^DL[0-9]{3,}$')
);

CREATE TABLE IF NOT EXISTS dealer_customer_links (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dealer_id           UUID NOT NULL REFERENCES dealers(dealer_id) ON DELETE RESTRICT,
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    first_application_at TIMESTAMPTZ,
    last_application_at  TIMESTAMPTZ,
    application_count   INTEGER NOT NULL DEFAULT 1 CHECK (application_count >= 0),
    relationship_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (relationship_status IN ('ACTIVE','INACTIVE','BLOCKED')),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (dealer_id, customer_id)
);

-- ---------------------------------------------------------------------------
-- GROUP 5 — LENDING  (Tables 13-14)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS loan_applications (
    application_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_ref     VARCHAR(20)  NOT NULL UNIQUE,
    customer_id         UUID NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    dealer_id           UUID REFERENCES dealers(dealer_id) ON DELETE SET NULL,
    requested_amount    NUMERIC(12,2) NOT NULL CHECK (requested_amount > 0),
    tenure_months       INTEGER NOT NULL CHECK (tenure_months BETWEEN 1 AND 360),
    application_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    application_status  application_status NOT NULL DEFAULT 'SUBMITTED',
    decision            decision,
    risk_score          NUMERIC(5,2) CHECK (risk_score BETWEEN 0 AND 100),
    fraud_score         NUMERIC(5,2) CHECK (fraud_score BETWEEN 0 AND 100),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_application_ref_format CHECK (application_ref ~ '^APP[0-9]{4,}$')
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id      UUID NOT NULL UNIQUE REFERENCES loan_applications(application_id) ON DELETE RESTRICT,
    loan_account_ref    VARCHAR(20)  NOT NULL UNIQUE,
    sanctioned_amount   NUMERIC(12,2) NOT NULL CHECK (sanctioned_amount > 0),
    disbursed_amount    NUMERIC(12,2) NOT NULL CHECK (disbursed_amount >= 0),
    interest_rate       NUMERIC(5,2)  CHECK (interest_rate BETWEEN 0 AND 100),
    tenure_months       INTEGER NOT NULL CHECK (tenure_months BETWEEN 1 AND 360),
    disbursement_date   DATE,
    loan_status         loan_status NOT NULL DEFAULT 'PENDING_DISBURSEMENT',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_loan_ref_format CHECK (loan_account_ref ~ '^LN[0-9]{4,}$'),
    CONSTRAINT chk_disbursed_lte_sanctioned CHECK (disbursed_amount <= sanctioned_amount)
);

-- ---------------------------------------------------------------------------
-- GROUP 6 — GUARANTOR NETWORK  (Tables 15-16)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS guarantors (
    guarantor_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guarantor_ref       VARCHAR(20)  NOT NULL UNIQUE,
    full_name           VARCHAR(200) NOT NULL,
    identity_hash       VARCHAR(128),
    mobile_id           UUID REFERENCES mobile_numbers(mobile_id) ON DELETE SET NULL,
    address_id          UUID REFERENCES addresses(address_id) ON DELETE SET NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_guarantor_ref_format CHECK (guarantor_ref ~ '^G[0-9]{3,}$')
);

CREATE TABLE IF NOT EXISTS loan_guarantors (
    link_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id      UUID NOT NULL REFERENCES loan_applications(application_id) ON DELETE RESTRICT,
    guarantor_id        UUID NOT NULL REFERENCES guarantors(guarantor_id) ON DELETE RESTRICT,
    relationship_type   VARCHAR(30) NOT NULL DEFAULT 'GUARANTOR' CHECK (relationship_type IN ('GUARANTOR','CO_APPLICANT','REFERENCE','OTHER')),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (application_id, guarantor_id)
);

-- ---------------------------------------------------------------------------
-- GROUP 7 — PAYMENTS  (Tables 17-18)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS payments (
    payment_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    loan_id             UUID NOT NULL REFERENCES loans(loan_id) ON DELETE RESTRICT,
    payment_date        DATE NOT NULL,
    amount              NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    payment_method      payment_method NOT NULL DEFAULT 'OTHER',
    payment_status      payment_status NOT NULL DEFAULT 'SUCCESS',
    days_past_due       INTEGER NOT NULL DEFAULT 0 CHECK (days_past_due >= 0),
    transaction_ref     VARCHAR(64),
    transaction_hash    VARCHAR(128),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS repayment_behaviour (
    behaviour_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    loan_id             UUID NOT NULL REFERENCES loans(loan_id) ON DELETE RESTRICT,
    avg_payment_delay_days NUMERIC(6,2) NOT NULL DEFAULT 0,
    missed_payment_count INTEGER NOT NULL DEFAULT 0 CHECK (missed_payment_count >= 0),
    early_payment_count INTEGER NOT NULL DEFAULT 0 CHECK (early_payment_count >= 0),
    partial_payment_count INTEGER NOT NULL DEFAULT 0 CHECK (partial_payment_count >= 0),
    bounce_count        INTEGER NOT NULL DEFAULT 0 CHECK (bounce_count >= 0),
    payment_velocity    NUMERIC(6,2),
    behaviour_score     NUMERIC(5,2) CHECK (behaviour_score BETWEEN 0 AND 100),
    calculated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (loan_id, calculated_at)
);

-- ---------------------------------------------------------------------------
-- GROUP 8 — LOCATION / ACTIVITY  (Tables 19-20)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS locations (
    location_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    latitude            NUMERIC(9,6),
    longitude           NUMERIC(9,6),
    city                VARCHAR(100),
    district            VARCHAR(100),
    state               VARCHAR(100),
    pincode             VARCHAR(10),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_loc_lat CHECK (latitude IS NULL OR (latitude BETWEEN -90 AND 90)),
    CONSTRAINT chk_loc_lon CHECK (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
);

CREATE TABLE IF NOT EXISTS application_events (
    event_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id      UUID REFERENCES loan_applications(application_id) ON DELETE SET NULL,
    customer_id         UUID REFERENCES customers(customer_id) ON DELETE SET NULL,
    device_id           UUID REFERENCES devices(device_id) ON DELETE SET NULL,
    ip_id               UUID REFERENCES ip_addresses(ip_id) ON DELETE SET NULL,
    location_id         UUID REFERENCES locations(location_id) ON DELETE SET NULL,
    event_type          VARCHAR(40) NOT NULL CHECK (event_type IN (
                            'APPLICATION_STARTED','APPLICATION_SUBMITTED','LOGIN',
                            'DEVICE_CHANGED','MOBILE_CHANGED','BANK_ACCOUNT_CHANGED',
                            'DOCUMENT_UPLOADED','APPLICATION_EDITED','LOCATION_CHANGED',
                            'OTP_VERIFIED','KYC_COMPLETED','CREDIT_CHECK','LOAN_DISBURSED',
                            'PAYMENT_MADE','PAYMENT_MISSED'
                        )),
    event_timestamp     TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- GROUP 9 — SWARM RELATIONSHIP NETWORK  (Table 21)  — CORE TABLE
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS entity_relationships (
    relationship_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_type  VARCHAR(30) NOT NULL CHECK (source_entity_type IN (
                            'CUSTOMER','MOBILE','DEVICE','BANK_ACCOUNT','ADDRESS',
                            'DEALER','GUARANTOR','IP','LOAN','APPLICATION','LOCATION'
                        )),
    source_entity_id    UUID NOT NULL,
    target_entity_type  VARCHAR(30) NOT NULL CHECK (target_entity_type IN (
                            'CUSTOMER','MOBILE','DEVICE','BANK_ACCOUNT','ADDRESS',
                            'DEALER','GUARANTOR','IP','LOAN','APPLICATION','LOCATION'
                        )),
    target_entity_id    UUID NOT NULL,
    relationship_type   VARCHAR(40) NOT NULL CHECK (relationship_type IN (
                            'SHARED_DEVICE','SHARED_MOBILE','SHARED_BANK_ACCOUNT',
                            'SHARED_ADDRESS','SHARED_GUARANTOR','SAME_IP','SAME_DEALER',
                            'SIMILAR_BEHAVIOUR','SUSPICIOUS_LINK','SHARED_LOCATION',
                            'SHARED_DEALER_DEVICE','FREQUENT_CO_LOCATION'
                        )),
    strength            NUMERIC(4,3) NOT NULL DEFAULT 0.5 CHECK (strength BETWEEN 0 AND 1),
    confidence          NUMERIC(4,3) NOT NULL DEFAULT 0.5 CHECK (confidence BETWEEN 0 AND 1),
    evidence_count      INTEGER NOT NULL DEFAULT 1 CHECK (evidence_count >= 0),
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_entity_type, source_entity_id, target_entity_type, target_entity_id, relationship_type),
    CONSTRAINT chk_no_self_ref CHECK (NOT (source_entity_type = target_entity_type AND source_entity_id = target_entity_id))
);

-- ---------------------------------------------------------------------------
-- GROUP 10 — FRAUD INTELLIGENCE  (Tables 22-23)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fraud_signals (
    signal_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type         VARCHAR(30) NOT NULL CHECK (entity_type IN (
                            'CUSTOMER','MOBILE','DEVICE','BANK_ACCOUNT','ADDRESS',
                            'DEALER','GUARANTOR','IP','LOAN','APPLICATION','LOCATION','CLUSTER'
                        )),
    entity_id           UUID NOT NULL,
    signal_type         VARCHAR(50) NOT NULL CHECK (signal_type IN (
                            'SHARED_DEVICE','IDENTITY_REUSE','MULTIPLE_MOBILE_LINK',
                            'MULTIPLE_BANK_ACCOUNT_LINK','UNUSUAL_DEALER_CLUSTER',
                            'LOCATION_ANOMALY','RAPID_APPLICATION_BURST','UNUSUAL_REPAYMENT_PATTERN',
                            'SHARED_BANK_ACCOUNT','SHARED_ADDRESS','SHARED_GUARANTOR',
                            'DEVICE_VELOCITY','IP_VELOCITY','BEHAVIOURAL_ANOMALY'
                        )),
    severity            signal_severity NOT NULL DEFAULT 'MEDIUM',
    score               NUMERIC(5,2) NOT NULL CHECK (score BETWEEN 0 AND 100),
    confidence          NUMERIC(4,3) NOT NULL DEFAULT 0.5 CHECK (confidence BETWEEN 0 AND 1),
    description         TEXT,
    detected_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at          TIMESTAMPTZ,
    evidence            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_expires_after_detected CHECK (expires_at IS NULL OR expires_at > detected_at)
);

CREATE TABLE IF NOT EXISTS risk_scores (
    risk_score_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type         VARCHAR(30) NOT NULL CHECK (entity_type IN (
                            'CUSTOMER','LOAN','APPLICATION','DEALER','DEVICE','CLUSTER'
                        )),
    entity_id           UUID NOT NULL,
    risk_score          NUMERIC(5,2) NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    fraud_probability   NUMERIC(5,4) NOT NULL CHECK (fraud_probability BETWEEN 0 AND 1),
    risk_level          risk_level NOT NULL,
    model_version       VARCHAR(30) NOT NULL,
    calculated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    feature_snapshot    JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
    -- no UNIQUE on (entity_type, entity_id, calculated_at) intentionally to preserve history;
    -- dedup handled by application; index enforces fast lookup
);

-- ---------------------------------------------------------------------------
-- GROUP 11 — FRAUD CLUSTERS  (Tables 24-25)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fraud_clusters (
    cluster_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_ref         VARCHAR(20)  NOT NULL UNIQUE,
    cluster_type        cluster_type NOT NULL DEFAULT 'MIXED_ENTITY_CLUSTER',
    risk_score          NUMERIC(5,2) CHECK (risk_score BETWEEN 0 AND 100),
    member_count        INTEGER NOT NULL DEFAULT 0 CHECK (member_count >= 0),
    cluster_status      cluster_status NOT NULL DEFAULT 'ACTIVE',
    detected_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_updated_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata            JSONB NOT NULL DEFAULT '{}',
    CONSTRAINT chk_cluster_ref_format CHECK (cluster_ref ~ '^F-[0-9]{4,}$')
);

CREATE TABLE IF NOT EXISTS fraud_cluster_members (
    member_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id          UUID NOT NULL REFERENCES fraud_clusters(cluster_id) ON DELETE CASCADE,
    entity_type         VARCHAR(30) NOT NULL CHECK (entity_type IN (
                            'CUSTOMER','MOBILE','DEVICE','BANK_ACCOUNT','ADDRESS',
                            'DEALER','GUARANTOR','IP','LOAN','APPLICATION'
                        )),
    entity_id           UUID NOT NULL,
    membership_score    NUMERIC(4,3) NOT NULL DEFAULT 0.5 CHECK (membership_score BETWEEN 0 AND 1),
    joined_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    left_at             TIMESTAMPTZ,
    UNIQUE (cluster_id, entity_type, entity_id),
    CONSTRAINT chk_left_after_joined CHECK (left_at IS NULL OR left_at > joined_at)
);

-- ---------------------------------------------------------------------------
-- GROUP 12 — ALERTS  (Table 26)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_ref           VARCHAR(20)  NOT NULL UNIQUE,
    entity_type         VARCHAR(30) CHECK (entity_type IN (
                            'CUSTOMER','LOAN','APPLICATION','DEALER','DEVICE','CLUSTER'
                        )),
    entity_id           UUID,
    cluster_id          UUID REFERENCES fraud_clusters(cluster_id) ON DELETE SET NULL,
    alert_type          VARCHAR(50) NOT NULL CHECK (alert_type IN (
                            'EMERGING_FRAUD_NETWORK','HIGH_RISK_DEVICE_CLUSTER',
                            'SHARED_BANK_ACCOUNT_NETWORK','DEALER_ANOMALY',
                            'RAPID_APPLICATION_CLUSTER','BEHAVIOURAL_ANOMALY',
                            'GUARANTOR_RING','LOCATION_ANOMALY','REPAYMENT_ANOMALY'
                        )),
    severity            alert_severity NOT NULL DEFAULT 'MEDIUM',
    risk_score          NUMERIC(5,2) CHECK (risk_score BETWEEN 0 AND 100),
    alert_status        alert_status NOT NULL DEFAULT 'OPEN',
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at         TIMESTAMPTZ,
    evidence            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_resolved_after_generated CHECK (resolved_at IS NULL OR resolved_at >= generated_at),
    CONSTRAINT chk_alert_ref_format CHECK (alert_ref ~ '^ALT-[0-9]{4,}$')
);

-- ---------------------------------------------------------------------------
-- GROUP 13 — INVESTIGATION  (Tables 27-28)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS investigations (
    investigation_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id            UUID NOT NULL REFERENCES fraud_alerts(alert_id) ON DELETE RESTRICT,
    investigator_ref    VARCHAR(100),
    investigation_status investigation_status NOT NULL DEFAULT 'OPEN',
    priority            investigation_priority NOT NULL DEFAULT 'MEDIUM',
    notes               TEXT,
    opened_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at           TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_closed_after_opened CHECK (closed_at IS NULL OR closed_at >= opened_at)
);

CREATE TABLE IF NOT EXISTS investigation_actions (
    action_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investigation_id    UUID NOT NULL REFERENCES investigations(investigation_id) ON DELETE CASCADE,
    action_type         VARCHAR(40) NOT NULL CHECK (action_type IN (
                            'NOTE_ADDED','STATUS_CHANGED','EVIDENCE_ADDED',
                            'ASSIGNED','ESCALATED','CONTACTED_CUSTOMER',
                            'CONTACTED_DEALER','FIELD_VISIT','DOCUMENT_VERIFIED',
                            'CASE_CLOSED','CASE_REOPENED','ALERT_LINKED'
                        )),
    performed_by        VARCHAR(100),
    notes               TEXT,
    performed_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- GROUP 14 — AI / MACHINE LEARNING  (Tables 29-30)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS model_versions (
    model_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name          VARCHAR(100) NOT NULL,
    version             VARCHAR(30)  NOT NULL,
    model_type          VARCHAR(50)  NOT NULL CHECK (model_type IN (
                            'FRAUD_CLASSIFIER','RISK_SCORER','CLUSTER_DETECTOR',
                            'BEHAVIOURAL_MODEL','NETWORK_EMBEDDING','ENSEMBLE','OTHER'
                        )),
    training_completed_at TIMESTAMPTZ,
    performance_metrics JSONB NOT NULL DEFAULT '{}',
    model_status        model_status NOT NULL DEFAULT 'TRAINING',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (model_name, version)
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id            UUID NOT NULL REFERENCES model_versions(model_id) ON DELETE RESTRICT,
    entity_type         VARCHAR(30) NOT NULL CHECK (entity_type IN (
                            'CUSTOMER','LOAN','APPLICATION','DEALER','DEVICE','CLUSTER'
                        )),
    entity_id           UUID NOT NULL,
    prediction_type     VARCHAR(50) NOT NULL,
    prediction_score    NUMERIC(6,4) NOT NULL CHECK (prediction_score BETWEEN 0 AND 1),
    prediction_label    VARCHAR(30),
    feature_snapshot    JSONB NOT NULL DEFAULT '{}',
    predicted_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- GROUP 15 — GOVERNANCE  (Table 31)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_ref            VARCHAR(100),
    action              VARCHAR(50) NOT NULL CHECK (action IN (
                            'CREATE','UPDATE','DELETE','VIEW','LOGIN','LOGOUT',
                            'APPROVE','REJECT','ESCALATE','EXPORT','IMPORT','OTHER'
                        )),
    entity_type         VARCHAR(30),
    entity_id           UUID,
    old_value           JSONB,
    new_value           JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- HELPER: updated_at auto-touch function + triggers
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_customers_updated ON customers;
CREATE TRIGGER trg_customers_updated BEFORE UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_dealers_updated ON dealers;
CREATE TRIGGER trg_dealers_updated BEFORE UPDATE ON dealers FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_dealer_customer_links_updated ON dealer_customer_links;
CREATE TRIGGER trg_dealer_customer_links_updated BEFORE UPDATE ON dealer_customer_links FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_loan_applications_updated ON loan_applications;
CREATE TRIGGER trg_loan_applications_updated BEFORE UPDATE ON loan_applications FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_loans_updated ON loans;
CREATE TRIGGER trg_loans_updated BEFORE UPDATE ON loans FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_entity_relationships_updated ON entity_relationships;
CREATE TRIGGER trg_entity_relationships_updated BEFORE UPDATE ON entity_relationships FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_fraud_clusters_updated ON fraud_clusters;
CREATE TRIGGER trg_fraud_clusters_updated BEFORE UPDATE ON fraud_clusters FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
DROP TRIGGER IF EXISTS trg_investigations_updated ON investigations;
CREATE TRIGGER trg_investigations_updated BEFORE UPDATE ON investigations FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
