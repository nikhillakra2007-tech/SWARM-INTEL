# Swarm Intelligence Lending Network

AI-driven lending fraud intelligence platform — discovers hidden relationships across lending entities and identifies emerging fraud ecosystems before traditional loan-level checks.

> Synthetic demo data only. Not a production fraud system.

## Architecture
```
Frontend → FastAPI → SQLAlchemy → PostgreSQL (31 tables) → Intelligence (graph / fraud / ML / clusters) → Alerts / Investigations
```
Local PostgreSQL now; Supabase PostgreSQL later via `DATABASE_URL` change only.

## Quick start

```powershell
# DB (once)
psql postgresql://postgres:postgres@localhost:5432/postgres -c "CREATE DATABASE swarm_lending"
.\database\scripts\setup.ps1   # applies schema + seeds

# Backend
cd backend
Copy-Item .env.example .env   # edit if needed
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# docs: http://127.0.0.1:8000/docs  health: /health
```

## Project layout
```
swarm/
  README.md          # ← this file (single project README)
  database/          # 31-table schema, seeds, queries, docs
  backend/           # FastAPI + SQLAlchemy + intelligence
  frontend/          # (next phase)
```

## Backend smoke
```powershell
cd backend
$env:PGPASSWORD="postgres"; python -m pytest tests -v
curl http://127.0.0.1:8000/health
```

## Key demo: F-1001 cluster
Customers C013–C016 share Device D004, Mobile M002, Bank B007, Address A013, Dealer DL003, Guarantor G005. Individually low-risk; collectively CRITICAL (risk 91.5). Reconstruct via `/api/relationships/CUSTOMER/{id}`, `/api/network/CUSTOMER/{id}`, `/api/clusters`, `/api/fraud/analyze/CUSTOMER/{id}`.

## Env
`DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending` — change host to Supabase when migrating.

## Tests
Database: connection + 31 tables + fraud network queries. Backend: 12 tests (health, CRUD, intelligence, ML features, cluster). All passing.
