-- =============================================================================
-- 002_types.sql — ENUM types for Swarm Intelligence Lending Network
-- =============================================================================
-- Stable categorical columns use ENUMs; polymorphic / open-ended columns
-- (entity_type, relationship_type, signal_type, etc.) intentionally use
-- VARCHAR + CHECK so new values can be added without a migration.
-- =============================================================================

DO $$ BEGIN CREATE TYPE gender AS ENUM ('MALE','FEMALE','OTHER','PREFER_NOT_TO_SAY'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE income_band AS ENUM ('LOW','LOWER_MIDDLE','MIDDLE','UPPER_MIDDLE','HIGH','UNKNOWN'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE customer_status AS ENUM ('ACTIVE','INACTIVE','BLOCKED','SUSPECT','CLOSED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE mobile_status AS ENUM ('ACTIVE','INACTIVE','SUSPECT','BLOCKED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE bank_account_type AS ENUM ('SAVINGS','CURRENT','SALARY','OTHER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE bank_account_status AS ENUM ('ACTIVE','DORMANT','CLOSED','FROZEN','SUSPECT'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE device_status AS ENUM ('ACTIVE','INACTIVE','SUSPECT','BLOCKED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE device_type AS ENUM ('MOBILE','TABLET','DESKTOP','LAPTOP','OTHER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE dealer_type AS ENUM ('DSA','BRANCH','ONLINE','BROKER','CORPORATE','OTHER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE dealer_status AS ENUM ('ACTIVE','INACTIVE','SUSPENDED','BLACKLISTED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE application_status AS ENUM ('DRAFT','SUBMITTED','UNDER_REVIEW','APPROVED','REJECTED','WITHDRAWN','PENDING'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE decision AS ENUM ('APPROVED','REJECTED','PENDING','REFER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE loan_status AS ENUM ('PENDING_DISBURSEMENT','ACTIVE','CLOSED','DEFAULTED','WRITTEN_OFF','FORECLOSED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE payment_status AS ENUM ('SUCCESS','FAILED','PENDING','REVERSED','PARTIAL'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE payment_method AS ENUM ('UPI','NEFT','IMPS','NACH','CASH','CHEQUE','CARD','WALLET','OTHER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE signal_severity AS ENUM ('LOW','MEDIUM','HIGH','CRITICAL'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE risk_level AS ENUM ('LOW','MEDIUM','HIGH','CRITICAL'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE cluster_status AS ENUM ('ACTIVE','UNDER_REVIEW','CONFIRMED_FRAUD','FALSE_POSITIVE','ARCHIVED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE cluster_type AS ENUM ('DEVICE_CLUSTER','MOBILE_CLUSTER','BANK_ACCOUNT_CLUSTER','DEALER_CLUSTER','MIXED_ENTITY_CLUSTER','BEHAVIOURAL_CLUSTER','OTHER'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE alert_severity AS ENUM ('LOW','MEDIUM','HIGH','CRITICAL'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE alert_status AS ENUM ('OPEN','ACKNOWLEDGED','IN_INVESTIGATION','RESOLVED','DISMISSED','ESCALATED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE investigation_status AS ENUM ('OPEN','IN_PROGRESS','ON_HOLD','CLOSED','ESCALATED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE investigation_priority AS ENUM ('LOW','MEDIUM','HIGH','URGENT'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE model_status AS ENUM ('TRAINING','EVALUATING','ACTIVE','RETIRED','FAILED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE ip_version AS ENUM ('V4','V6'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
