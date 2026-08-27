-- =============================================================================
-- fraud_network_queries.sql — 10 fraud-network demonstration queries
-- Swarm Intelligence Lending Network — PostgreSQL / Supabase compatible
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Q1: Which customers share a device?
-- ---------------------------------------------------------------------------
-- Finds all customer pairs that share at least one device, with device detail.
SELECT
    c1.customer_ref AS customer_a,
    c2.customer_ref AS customer_b,
    d.device_fingerprint,
    d.device_id
FROM customer_device_links cdl1
JOIN customer_device_links cdl2
  ON cdl1.device_id = cdl2.device_id AND cdl1.customer_id < cdl2.customer_id
JOIN customers c1 ON c1.customer_id = cdl1.customer_id
JOIN customers c2 ON c2.customer_id = cdl2.customer_id
JOIN devices d ON d.device_id = cdl1.device_id
ORDER BY d.device_fingerprint, c1.customer_ref;

-- Alternative via swarm graph (includes strength/confidence):
-- SELECT source_entity_id, target_entity_id, strength FROM entity_relationships
-- WHERE relationship_type='SHARED_DEVICE';

-- ---------------------------------------------------------------------------
-- Q2: Which customers share a mobile number?
-- ---------------------------------------------------------------------------
SELECT
    c1.customer_ref AS customer_a,
    c2.customer_ref AS customer_b,
    m.mobile_id,
    m.mobile_hash
FROM customer_mobile_links cml1
JOIN customer_mobile_links cml2
  ON cml1.mobile_id = cml2.mobile_id AND cml1.customer_id < cml2.customer_id
JOIN customers c1 ON c1.customer_id = cml1.customer_id
JOIN customers c2 ON c2.customer_id = cml2.customer_id
JOIN mobile_numbers m ON m.mobile_id = cml1.mobile_id
ORDER BY m.mobile_id, c1.customer_ref;

-- ---------------------------------------------------------------------------
-- Q3: Which customers share a bank account?
-- ---------------------------------------------------------------------------
SELECT
    c1.customer_ref AS customer_a,
    c2.customer_ref AS customer_b,
    b.bank_name,
    b.bank_account_id
FROM customer_bank_links cbl1
JOIN customer_bank_links cbl2
  ON cbl1.bank_account_id = cbl2.bank_account_id AND cbl1.customer_id < cbl2.customer_id
JOIN customers c1 ON c1.customer_id = cbl1.customer_id
JOIN customers c2 ON c2.customer_id = cbl2.customer_id
JOIN bank_accounts b ON b.bank_account_id = cbl1.bank_account_id
ORDER BY b.bank_account_id, c1.customer_ref;

-- ---------------------------------------------------------------------------
-- Q4: Which dealers are connected to unusually large customer networks?
-- ---------------------------------------------------------------------------
-- Dealers with customer count > 2x average, sorted by exposure.
WITH dealer_stats AS (
    SELECT dealer_id, count(DISTINCT customer_id)::int AS customer_cnt
    FROM dealer_customer_links GROUP BY dealer_id
), avg_cnt AS (
    SELECT avg(customer_cnt) AS avg_customers FROM dealer_stats
)
SELECT
    d.dealer_code,
    d.dealer_name,
    ds.customer_cnt,
    round(ds.customer_cnt / NULLIF(ac.avg_customers,0), 2) AS times_avg,
    d.dealer_status
FROM dealer_stats ds
JOIN dealers d ON d.dealer_id = ds.dealer_id
CROSS JOIN avg_cnt ac
WHERE ds.customer_cnt > ac.avg_customers * 1.5
ORDER BY ds.customer_cnt DESC;

-- Using the view:
-- SELECT * FROM dealer_risk_overview ORDER BY distinct_customers DESC;

-- ---------------------------------------------------------------------------
-- Q5: Which devices connect multiple high-risk customers?
-- ---------------------------------------------------------------------------
SELECT
    d.device_fingerprint,
    d.device_id,
    count(DISTINCT c.customer_id)::int AS high_risk_customers,
    array_agg(DISTINCT c.customer_ref ORDER BY c.customer_ref) AS customer_refs,
    max(rs.risk_score) AS max_risk
FROM devices d
JOIN customer_device_links cdl ON cdl.device_id = d.device_id
JOIN customers c ON c.customer_id = cdl.customer_id
JOIN risk_scores rs ON rs.entity_type='CUSTOMER' AND rs.entity_id = c.customer_id
    AND rs.calculated_at = (SELECT max(rs2.calculated_at) FROM risk_scores rs2 WHERE rs2.entity_type='CUSTOMER' AND rs2.entity_id=c.customer_id)
WHERE rs.risk_level IN ('HIGH','CRITICAL')
GROUP BY d.device_id, d.device_fingerprint
HAVING count(DISTINCT c.customer_id) >= 2
ORDER BY high_risk_customers DESC, max_risk DESC;

-- View shortcut:
-- SELECT * FROM device_customer_network WHERE has_high_risk_customer AND linked_customers >= 2;

-- ---------------------------------------------------------------------------
-- Q6: Which customers belong to the same fraud cluster?
-- ---------------------------------------------------------------------------
SELECT
    fc.cluster_ref,
    fc.cluster_status,
    fc.risk_score AS cluster_risk,
    c.customer_ref,
    c.full_name,
    fcm.membership_score,
    fcm.joined_at
FROM fraud_clusters fc
JOIN fraud_cluster_members fcm ON fcm.cluster_id = fc.cluster_id AND fcm.entity_type='CUSTOMER'
JOIN customers c ON c.customer_id = fcm.entity_id
WHERE fcm.left_at IS NULL
ORDER BY fc.cluster_ref, fcm.membership_score DESC;

-- Pairs within same cluster:
-- SELECT c1.customer_ref, c2.customer_ref, fcm1.cluster_id
-- FROM fraud_cluster_members fcm1 JOIN fraud_cluster_members fcm2
--   ON fcm1.cluster_id=fcm2.cluster_id AND fcm1.entity_id < fcm2.entity_id
-- WHERE fcm1.entity_type='CUSTOMER' AND fcm2.entity_type='CUSTOMER';

-- ---------------------------------------------------------------------------
-- Q7: What relationships surround a suspicious customer? (e.g. C013)
-- ---------------------------------------------------------------------------
-- :customer_ref = 'C013'
WITH target AS (SELECT customer_id FROM customers WHERE customer_ref='C013')
SELECT
    er.relationship_type,
    er.target_entity_type,
    er.target_entity_id,
    er.strength,
    er.confidence,
    er.evidence_count,
    -- Resolve target label where possible
    coalesce(c.customer_ref, m.mobile_hash, b.account_hash, d.device_fingerprint, dl.dealer_code, g.guarantor_ref) AS target_label
FROM entity_relationships er
JOIN target t ON er.source_entity_type='CUSTOMER' AND er.source_entity_id = t.customer_id
LEFT JOIN customers c ON er.target_entity_type='CUSTOMER' AND c.customer_id=er.target_entity_id
LEFT JOIN mobile_numbers m ON er.target_entity_type='MOBILE' AND m.mobile_id=er.target_entity_id
LEFT JOIN bank_accounts b ON er.target_entity_type='BANK_ACCOUNT' AND b.bank_account_id=er.target_entity_id
LEFT JOIN devices d ON er.target_entity_type='DEVICE' AND d.device_id=er.target_entity_id
LEFT JOIN dealers dl ON er.target_entity_type='DEALER' AND dl.dealer_id=er.target_entity_id
LEFT JOIN guarantors g ON er.target_entity_type='GUARANTOR' AND g.guarantor_id=er.target_entity_id
ORDER BY er.strength DESC;

-- ---------------------------------------------------------------------------
-- Q8: Which clusters are rapidly growing? (members added in last 7 days vs prior)
-- ---------------------------------------------------------------------------
SELECT
    fc.cluster_ref,
    fc.cluster_status,
    count(*) FILTER (WHERE fcm.joined_at >= now() - interval '7 days')::int  AS added_last_7d,
    count(*) FILTER (WHERE fcm.joined_at <  now() - interval '7 days')::int  AS added_before,
    count(*)::int AS total_members,
    CASE WHEN count(*) FILTER (WHERE fcm.joined_at < now() - interval '7 days') = 0
         THEN NULL
         ELSE round(count(*) FILTER (WHERE fcm.joined_at >= now() - interval '7 days')::numeric
                    / NULLIF(count(*) FILTER (WHERE fcm.joined_at < now() - interval '7 days'),0), 2)
    END AS growth_ratio
FROM fraud_clusters fc
JOIN fraud_cluster_members fcm ON fcm.cluster_id = fc.cluster_id AND fcm.left_at IS NULL
GROUP BY fc.cluster_id, fc.cluster_ref, fc.cluster_status
HAVING count(*) FILTER (WHERE fcm.joined_at >= now() - interval '7 days') > 0
ORDER BY added_last_7d DESC;

-- ---------------------------------------------------------------------------
-- Q9: Which customers experienced a sudden increase in risk?
-- ---------------------------------------------------------------------------
-- Customers whose latest risk is >= 20 points above their score 14 days earlier.
WITH ranked AS (
    SELECT
        c.customer_ref,
        rs.risk_score,
        rs.calculated_at,
        lag(rs.risk_score) OVER (PARTITION BY rs.entity_id ORDER BY rs.calculated_at) AS prev_score,
        lag(rs.calculated_at) OVER (PARTITION BY rs.entity_id ORDER BY rs.calculated_at) AS prev_at
    FROM risk_scores rs
    JOIN customers c ON c.customer_id = rs.entity_id
    WHERE rs.entity_type='CUSTOMER'
)
SELECT customer_ref, prev_score, risk_score,
       (risk_score - prev_score) AS delta,
       calculated_at AS latest_at, prev_at
FROM ranked
WHERE prev_score IS NOT NULL AND (risk_score - prev_score) >= 20
ORDER BY delta DESC;

-- ---------------------------------------------------------------------------
-- Q10: Show the strongest connections around a suspicious entity (graph expansion)
-- ---------------------------------------------------------------------------
-- Top-10 strongest relationships for any entity in cluster F-1001, ordered by strength.
SELECT
    er.relationship_type,
    er.source_entity_type || ':' || left(er.source_entity_id::text,8) AS source,
    er.target_entity_type || ':' || left(er.target_entity_id::text,8) AS target,
    er.strength,
    er.confidence,
    er.evidence_count
FROM entity_relationships er
WHERE er.source_entity_id IN (SELECT entity_id FROM fraud_cluster_members WHERE cluster_id = (SELECT cluster_id FROM fraud_clusters WHERE cluster_ref='F-1001'))
   OR er.target_entity_id IN (SELECT entity_id FROM fraud_cluster_members WHERE cluster_id = (SELECT cluster_id FROM fraud_clusters WHERE cluster_ref='F-1001'))
ORDER BY er.strength DESC, er.confidence DESC
LIMIT 10;

-- Full cluster graph as adjacency list:
-- SELECT fc.cluster_ref, er.* FROM fraud_clusters fc
-- JOIN fraud_cluster_members fcm ON fcm.cluster_id=fc.cluster_id
-- JOIN entity_relationships er ON er.source_entity_id=fcm.entity_id OR er.target_entity_id=fcm.entity_id
-- WHERE fc.cluster_ref='F-1001' ORDER BY er.strength DESC;
