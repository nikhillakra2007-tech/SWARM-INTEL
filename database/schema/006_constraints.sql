-- =============================================================================
-- 006_constraints.sql — Extra constraints & data-quality helpers
-- =============================================================================
-- Most CHECK / UNIQUE / FK constraints are declared inline in 003_tables.sql.
-- This file adds any cross-cutting helpers and documents cascade policy.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Cascade policy summary (for documentation / review):
--   ON DELETE RESTRICT — financial / identity history is preserved
--     customers, mobile_numbers, bank_accounts, devices, loans,
--     loan_applications, fraud_alerts, model_versions
--   ON DELETE SET NULL — optional references where orphaning is acceptable
--     dealers.address_id, loan_applications.dealer_id,
--     guarantors.mobile_id / address_id, application_events.*_id,
--     fraud_alerts.cluster_id
--   ON DELETE CASCADE — composition children that have no meaning alone
--     fraud_cluster_members → fraud_clusters
--     investigation_actions → investigations
-- ---------------------------------------------------------------------------

-- ---------------------------------------------------------------------------
-- Optional: ensure risk_score / fraud_score produce consistent risk_level
-- (application-level; trigger-based example commented for transparency)
-- ---------------------------------------------------------------------------

-- Example: derive risk_level from risk_score automatically (uncomment to enable)
-- CREATE OR REPLACE FUNCTION derive_risk_level() RETURNS TRIGGER AS $$
-- BEGIN
--   IF NEW.risk_score < 30 THEN NEW.risk_level := 'LOW';
--   ELSIF NEW.risk_score < 60 THEN NEW.risk_level := 'MEDIUM';
--   ELSIF NEW.risk_score < 80 THEN NEW.risk_level := 'HIGH';
--   ELSE NEW.risk_level := 'CRITICAL';
--   END IF;
--   RETURN NEW;
-- END; $$ LANGUAGE plpgsql;
--
-- DROP TRIGGER IF EXISTS trg_risk_scores_level ON risk_scores;
-- CREATE TRIGGER trg_risk_scores_level BEFORE INSERT OR UPDATE ON risk_scores
-- FOR EACH ROW EXECUTE FUNCTION derive_risk_level();

-- ---------------------------------------------------------------------------
-- Data-quality: prevent identical hashes re-used with different casing
-- (hash columns are UNIQUE already; this is a reminder that hashes should be
--  lower-cased at write time)
-- ---------------------------------------------------------------------------

SELECT '006_constraints.sql — cascade policy documented, no extra DDL required' AS status;
