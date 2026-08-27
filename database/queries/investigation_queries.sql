-- investigation_queries.sql — Alert & investigation queries

-- Open alerts with cluster context
SELECT * FROM active_fraud_alerts ORDER BY severity DESC, generated_at DESC;

-- Investigations with latest action
SELECT i.investigation_id, fa.alert_ref, i.investigation_status, i.priority,
       (SELECT max(performed_at) FROM investigation_actions ia WHERE ia.investigation_id=i.investigation_id) AS last_action_at
FROM investigations i JOIN fraud_alerts fa ON fa.alert_id=i.alert_id
ORDER BY i.opened_at DESC;

-- Audit trail for a specific investigation (replace INV id)
-- SELECT * FROM investigation_actions WHERE investigation_id = '...' ORDER BY performed_at;
