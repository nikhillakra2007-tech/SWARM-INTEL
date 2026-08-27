-- =============================================================================
-- 007_views.sql — Dashboard / API views for Swarm Intelligence Lending Network
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 1. customer_risk_overview — latest risk per customer + vitals
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW customer_risk_overview AS
SELECT
    c.customer_id,
    c.customer_ref,
    c.full_name,
    c.customer_status,
    c.income_band,
    latest.risk_score  AS latest_risk_score,
    latest.risk_level  AS latest_risk_level,
    latest.fraud_probability AS latest_fraud_probability,
    latest.calculated_at     AS risk_calculated_at,
    cnt_apps.app_count,
    cnt_loans.loan_count,
    cnt_signals.open_signal_count
FROM customers c
LEFT JOIN LATERAL (
    SELECT rs.risk_score, rs.risk_level, rs.fraud_probability, rs.calculated_at
    FROM risk_scores rs
    WHERE rs.entity_type = 'CUSTOMER' AND rs.entity_id = c.customer_id
    ORDER BY rs.calculated_at DESC LIMIT 1
) latest ON true
LEFT JOIN LATERAL (
    SELECT count(*)::int AS app_count FROM loan_applications la WHERE la.customer_id = c.customer_id
) cnt_apps ON true
LEFT JOIN LATERAL (
    SELECT count(*)::int AS loan_count FROM loans l
    JOIN loan_applications la2 ON la2.application_id = l.application_id
    WHERE la2.customer_id = c.customer_id
) cnt_loans ON true
LEFT JOIN LATERAL (
    SELECT count(*)::int AS open_signal_count FROM fraud_signals fs
    WHERE fs.entity_type = 'CUSTOMER' AND fs.entity_id = c.customer_id
      AND (fs.expires_at IS NULL OR fs.expires_at > now())
) cnt_signals ON true;

-- ---------------------------------------------------------------------------
-- 2. active_fraud_alerts — unresolved alerts enriched with cluster info
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW active_fraud_alerts AS
SELECT
    fa.alert_id,
    fa.alert_ref,
    fa.entity_type,
    fa.entity_id,
    fa.cluster_id,
    fc.cluster_ref,
    fc.cluster_status,
    fa.alert_type,
    fa.severity,
    fa.risk_score,
    fa.alert_status,
    fa.generated_at,
    fa.evidence
FROM fraud_alerts fa
LEFT JOIN fraud_clusters fc ON fc.cluster_id = fa.cluster_id
WHERE fa.alert_status IN ('OPEN','ACKNOWLEDGED','IN_INVESTIGATION','ESCALATED');

-- ---------------------------------------------------------------------------
-- 3. fraud_cluster_overview — cluster summary with member counts
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW fraud_cluster_overview AS
SELECT
    fc.cluster_id,
    fc.cluster_ref,
    fc.cluster_type,
    fc.cluster_status,
    fc.risk_score,
    fc.member_count,
    fc.detected_at,
    fc.last_updated_at,
    (SELECT count(*)::int FROM fraud_cluster_members fcm WHERE fcm.cluster_id = fc.cluster_id AND fcm.left_at IS NULL) AS active_members,
    (SELECT count(*)::int FROM fraud_alerts fa WHERE fa.cluster_id = fc.cluster_id AND fa.alert_status IN ('OPEN','ACKNOWLEDGED','IN_INVESTIGATION')) AS open_alerts
FROM fraud_clusters fc;

-- ---------------------------------------------------------------------------
-- 4. customer_network_connections — one-hop links from each customer
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW customer_network_connections AS
SELECT
    c.customer_id,
    c.customer_ref,
    er.relationship_type,
    er.target_entity_type,
    er.target_entity_id,
    er.strength,
    er.confidence,
    er.evidence_count,
    er.first_seen,
    er.last_seen
FROM customers c
JOIN entity_relationships er
  ON er.source_entity_type = 'CUSTOMER' AND er.source_entity_id = c.customer_id
UNION ALL
SELECT
    c2.customer_id,
    c2.customer_ref,
    er2.relationship_type,
    er2.source_entity_type AS target_entity_type,
    er2.source_entity_id   AS target_entity_id,
    er2.strength,
    er2.confidence,
    er2.evidence_count,
    er2.first_seen,
    er2.last_seen
FROM customers c2
JOIN entity_relationships er2
  ON er2.target_entity_type = 'CUSTOMER' AND er2.target_entity_id = c2.customer_id;

-- ---------------------------------------------------------------------------
-- 5. dealer_risk_overview — dealer + exposure + avg customer risk
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW dealer_risk_overview AS
SELECT
    d.dealer_id,
    d.dealer_code,
    d.dealer_name,
    d.dealer_type,
    d.dealer_status,
    count(DISTINCT la.customer_id)::int       AS distinct_customers,
    count(DISTINCT la.application_id)::int    AS total_applications,
    count(DISTINCT l.loan_id)::int            AS total_loans,
    coalesce(avg(rs.risk_score), 0)::numeric(5,2) AS avg_customer_risk,
    max(rs.risk_score)                        AS max_customer_risk,
    count(DISTINCT CASE WHEN rs.risk_level IN ('HIGH','CRITICAL') THEN la.customer_id END)::int AS high_risk_customers
FROM dealers d
LEFT JOIN loan_applications la ON la.dealer_id = d.dealer_id
LEFT JOIN loans l ON l.application_id = la.application_id
LEFT JOIN risk_scores rs ON rs.entity_type = 'CUSTOMER' AND rs.entity_id = la.customer_id
        AND rs.calculated_at = (SELECT max(rs2.calculated_at) FROM risk_scores rs2 WHERE rs2.entity_type='CUSTOMER' AND rs2.entity_id=la.customer_id)
GROUP BY d.dealer_id, d.dealer_code, d.dealer_name, d.dealer_type, d.dealer_status;

-- ---------------------------------------------------------------------------
-- 6. device_customer_network — each device with its customer reach
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW device_customer_network AS
SELECT
    dev.device_id,
    dev.device_fingerprint,
    dev.device_type,
    dev.device_status,
    count(DISTINCT cdl.customer_id)::int AS linked_customers,
    array_agg(DISTINCT c.customer_ref ORDER BY c.customer_ref) AS customer_refs,
    max(rs.risk_score) AS max_linked_risk,
    bool_or(rs.risk_level IN ('HIGH','CRITICAL')) AS has_high_risk_customer
FROM devices dev
LEFT JOIN customer_device_links cdl ON cdl.device_id = dev.device_id
LEFT JOIN customers c ON c.customer_id = cdl.customer_id
LEFT JOIN risk_scores rs ON rs.entity_type='CUSTOMER' AND rs.entity_id = c.customer_id
        AND rs.calculated_at = (SELECT max(rs2.calculated_at) FROM risk_scores rs2 WHERE rs2.entity_type='CUSTOMER' AND rs2.entity_id=c.customer_id)
GROUP BY dev.device_id, dev.device_fingerprint, dev.device_type, dev.device_status;
