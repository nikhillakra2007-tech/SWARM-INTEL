-- =============================================================================
-- 005_indexes.sql — Indexing strategy for Swarm Intelligence Lending Network
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Customer / Identity lookups
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_customers_status          ON customers(customer_status);
CREATE INDEX IF NOT EXISTS idx_customers_created         ON customers(created_at);

CREATE INDEX IF NOT EXISTS idx_cml_customer              ON customer_mobile_links(customer_id);
CREATE INDEX IF NOT EXISTS idx_cml_mobile                ON customer_mobile_links(mobile_id);
CREATE INDEX IF NOT EXISTS idx_cml_primary               ON customer_mobile_links(customer_id) WHERE is_primary = true;

CREATE INDEX IF NOT EXISTS idx_cal_customer              ON customer_address_links(customer_id);
CREATE INDEX IF NOT EXISTS idx_cal_address               ON customer_address_links(address_id);

CREATE INDEX IF NOT EXISTS idx_cbl_customer              ON customer_bank_links(customer_id);
CREATE INDEX IF NOT EXISTS idx_cbl_bank                  ON customer_bank_links(bank_account_id);

CREATE INDEX IF NOT EXISTS idx_cdl_customer              ON customer_device_links(customer_id);
CREATE INDEX IF NOT EXISTS idx_cdl_device                ON customer_device_links(device_id);

-- ---------------------------------------------------------------------------
-- Financial / Dealer
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_dealers_status            ON dealers(dealer_status);
CREATE INDEX IF NOT EXISTS idx_dcl_dealer                ON dealer_customer_links(dealer_id);
CREATE INDEX IF NOT EXISTS idx_dcl_customer              ON dealer_customer_links(customer_id);

-- ---------------------------------------------------------------------------
-- Lending
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_applications_customer     ON loan_applications(customer_id);
CREATE INDEX IF NOT EXISTS idx_applications_dealer       ON loan_applications(dealer_id);
CREATE INDEX IF NOT EXISTS idx_applications_status       ON loan_applications(application_status);
CREATE INDEX IF NOT EXISTS idx_applications_timestamp    ON loan_applications(application_timestamp);
CREATE INDEX IF NOT EXISTS idx_applications_customer_ts  ON loan_applications(customer_id, application_timestamp);

CREATE INDEX IF NOT EXISTS idx_loans_application         ON loans(application_id);
CREATE INDEX IF NOT EXISTS idx_loans_status              ON loans(loan_status);

CREATE INDEX IF NOT EXISTS idx_loan_guarantors_app       ON loan_guarantors(application_id);
CREATE INDEX IF NOT EXISTS idx_loan_guarantors_guar      ON loan_guarantors(guarantor_id);

-- ---------------------------------------------------------------------------
-- Payments & behaviour
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_payments_loan             ON payments(loan_id);
CREATE INDEX IF NOT EXISTS idx_payments_date             ON payments(payment_date);
CREATE INDEX IF NOT EXISTS idx_payments_status           ON payments(payment_status);

CREATE INDEX IF NOT EXISTS idx_repay_behaviour_loan      ON repayment_behaviour(loan_id);
CREATE INDEX IF NOT EXISTS idx_repay_behaviour_calc      ON repayment_behaviour(calculated_at);

-- ---------------------------------------------------------------------------
-- Events (behavioural)
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_app_events_customer_ts    ON application_events(customer_id, event_timestamp);
CREATE INDEX IF NOT EXISTS idx_app_events_device_ts      ON application_events(device_id, event_timestamp);
CREATE INDEX IF NOT EXISTS idx_app_events_app            ON application_events(application_id);
CREATE INDEX IF NOT EXISTS idx_app_events_ip             ON application_events(ip_id);
CREATE INDEX IF NOT EXISTS idx_app_events_location       ON application_events(location_id);
CREATE INDEX IF NOT EXISTS idx_app_events_type           ON application_events(event_type);
CREATE INDEX IF NOT EXISTS idx_app_events_timestamp      ON application_events(event_timestamp);

-- ---------------------------------------------------------------------------
-- Swarm intelligence — entity_relationships (bidirectional graph traversal)
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_er_source                 ON entity_relationships(source_entity_type, source_entity_id);
CREATE INDEX IF NOT EXISTS idx_er_target                 ON entity_relationships(target_entity_type, target_entity_id);
CREATE INDEX IF NOT EXISTS idx_er_type                  ON entity_relationships(relationship_type);
CREATE INDEX IF NOT EXISTS idx_er_strength              ON entity_relationships(strength);
CREATE INDEX IF NOT EXISTS idx_er_confidence            ON entity_relationships(confidence);

-- ---------------------------------------------------------------------------
-- Fraud signals / risk scores
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fraud_signals_entity      ON fraud_signals(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_fraud_signals_type        ON fraud_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_fraud_signals_severity    ON fraud_signals(severity);
CREATE INDEX IF NOT EXISTS idx_fraud_signals_detected    ON fraud_signals(detected_at);

CREATE INDEX IF NOT EXISTS idx_risk_scores_entity        ON risk_scores(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_risk_scores_level         ON risk_scores(risk_level);
CREATE INDEX IF NOT EXISTS idx_risk_scores_calculated    ON risk_scores(calculated_at);
CREATE INDEX IF NOT EXISTS idx_risk_scores_entity_calc   ON risk_scores(entity_type, entity_id, calculated_at DESC);

-- ---------------------------------------------------------------------------
-- Fraud clusters & members (bidirectional)
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fcm_cluster               ON fraud_cluster_members(cluster_id);
CREATE INDEX IF NOT EXISTS idx_fcm_entity                ON fraud_cluster_members(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_fcm_joined                ON fraud_cluster_members(joined_at);

CREATE INDEX IF NOT EXISTS idx_clusters_status           ON fraud_clusters(cluster_status);
CREATE INDEX IF NOT EXISTS idx_clusters_type             ON fraud_clusters(cluster_type);
CREATE INDEX IF NOT EXISTS idx_clusters_risk             ON fraud_clusters(risk_score);
CREATE INDEX IF NOT EXISTS idx_clusters_detected         ON fraud_clusters(detected_at);

-- ---------------------------------------------------------------------------
-- Alerts / Investigations / Predictions
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_alerts_entity             ON fraud_alerts(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_alerts_cluster            ON fraud_alerts(cluster_id);
CREATE INDEX IF NOT EXISTS idx_alerts_status             ON fraud_alerts(alert_status);
CREATE INDEX IF NOT EXISTS idx_alerts_severity           ON fraud_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_type               ON fraud_alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_generated          ON fraud_alerts(generated_at);

CREATE INDEX IF NOT EXISTS idx_investigations_alert      ON investigations(alert_id);
CREATE INDEX IF NOT EXISTS idx_investigations_status     ON investigations(investigation_status);

CREATE INDEX IF NOT EXISTS idx_inv_actions_investigation ON investigation_actions(investigation_id);
CREATE INDEX IF NOT EXISTS idx_inv_actions_performed     ON investigation_actions(performed_at);

CREATE INDEX IF NOT EXISTS idx_predictions_entity        ON predictions(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_predictions_model         ON predictions(model_id);
CREATE INDEX IF NOT EXISTS idx_predictions_predicted     ON predictions(predicted_at);

CREATE INDEX IF NOT EXISTS idx_model_versions_status     ON model_versions(model_status);
CREATE INDEX IF NOT EXISTS idx_model_versions_name       ON model_versions(model_name);

-- ---------------------------------------------------------------------------
-- Governance
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_audit_entity              ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_action              ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_created             ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_user                ON audit_logs(user_ref);

-- ---------------------------------------------------------------------------
-- General created_at helpers
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_devices_fingerprint       ON devices(device_fingerprint);
CREATE INDEX IF NOT EXISTS idx_dealers_code              ON dealers(dealer_code);
CREATE INDEX IF NOT EXISTS idx_ip_hash                  ON ip_addresses(ip_hash);
