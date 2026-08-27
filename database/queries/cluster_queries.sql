-- cluster_queries.sql — Fraud cluster queries

-- All clusters with active member count
SELECT * FROM fraud_cluster_overview ORDER BY risk_score DESC;

-- Members of F-1001 with labels
SELECT fc.cluster_ref, fcm.entity_type, fcm.entity_id, fcm.membership_score
FROM fraud_clusters fc JOIN fraud_cluster_members fcm ON fcm.cluster_id=fc.cluster_id
WHERE fc.cluster_ref='F-1001' AND fcm.left_at IS NULL ORDER BY fcm.membership_score DESC;

-- Clusters that share an entity (bridge detection)
SELECT fcm1.cluster_id AS cluster_a, fcm2.cluster_id AS cluster_b,
       fcm1.entity_type, fcm1.entity_id, count(*)::int AS shared_entities
FROM fraud_cluster_members fcm1 JOIN fraud_cluster_members fcm2
  ON fcm1.entity_type=fcm2.entity_type AND fcm1.entity_id=fcm2.entity_id AND fcm1.cluster_id < fcm2.cluster_id
GROUP BY 1,2,3,4;
