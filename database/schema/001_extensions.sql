-- =============================================================================
-- 001_extensions.sql — PostgreSQL extensions for Swarm Intelligence Lending Network
-- =============================================================================
-- Enables UUID generation and optional full-text / trigram helpers.
-- All extensions are available on vanilla PostgreSQL and Supabase PostgreSQL.
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";      -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";     -- uuid_generate_v4() fallback
-- Optional but harmless on Supabase; comment out if unavailable:
-- CREATE EXTENSION IF NOT EXISTS "pg_trgm";
