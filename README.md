# SWARM•INTEL — Swarm Intelligence Lending Network

> **Detect the network. Understand the signal. Stop the fraud.**

SWARM•INTEL is an AI-driven lending fraud intelligence platform designed to identify hidden relationships and coordinated fraud patterns across the lending ecosystem before traditional loan-level checks.

Instead of evaluating a loan application only as an isolated record, SWARM•INTEL analyzes the **network surrounding an entity** — customers, devices, mobile numbers, addresses, bank accounts, dealers, applications, loans, guarantors, locations, and repayment behavior.

---

## 🌐 Live Demo & Deployment

| Resource | Link | Status |
|---|---|---|
| 🌐 **Live Web App (Vercel)** | [**Open SWARM•INTEL**](https://swarm-intel-app.vercel.app/) | ✅ **Active & Ready** |
| 💻 **GitHub Repository** | [nikhillakra2007-tech/SWARM-INTEL](https://github.com/nikhillakra2007-tech/SWARM-INTEL) | ✅ **Main** |

- **Production URL**: [https://swarm-intel-app.vercel.app](https://swarm-intel-app.vercel.app/)
- **Resilience**: The frontend is fully decoupled with zero-downtime interactive fallback simulation for all 31 database entity types, graph explorers, and fraud analysis engines.

---

## 📸 Platform Preview

### Intelligence Dashboard
The dashboard provides a real-time command center:
- **Active Fraud Networks & Clusters** (Connected components)
- **High-Risk Entities & Alerts**
- **Collective Risk Scoring & Donut Distributions**
- **Fraud Risk Velocity & Application Trends**
- **Top Fraud Signals & Risky Clusters**
- **Recent Intelligence Activity & Investigation Tracking**

### Network Intelligence
The platform builds and maps graph relationships:
```text
Customer ──► Device ──► Mobile ──► Bank Account ──► Dealer ──► Loan
```

---

## 🏛️ Architecture

```
Frontend (React 19 + TypeScript + Vite + Lenis) 
   │
   ├─► FastAPI (Backend) → SQLAlchemy → PostgreSQL (31 tables)
   │        └─► Intelligence Engine (Graph / Fraud Rules / ML / Clusters)
   │
   └─► Resilient Client Layer (Zero-downtime interactive demo on Vercel)
```

- **Frontend**: Modern React 19, TypeScript, Vite, Lenis smooth scrolling, Dark/Light/System themes, SVG network graph visualizers, entity analyzer.
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL (31 tables).
- **Intelligence**: Rule-based fraud signals + Graph analysis + `fraud_model_v2` GradientBoosting ML predictions + Collective Risk Engine ($0.25 \times \text{Individual} + 0.45 \times \text{Network} + 0.30 \times \text{ML}$).

---

## ⚡ Quick Start

### 1. Frontend
```powershell
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### 2. Database & Backend
```powershell
# Database setup (PostgreSQL)
psql postgresql://postgres:postgres@localhost:5432/postgres -c "CREATE DATABASE swarm_lending"
.\database\scripts\setup.ps1   # applies schema + seeds

# Backend setup (FastAPI)
cd backend
Copy-Item .env.example .env   # edit if needed
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Docs: http://127.0.0.1:8000/docs | Health: http://127.0.0.1:8000/health
```

---

## 🔍 Key Demo: F-1001 Fraud Cluster

- **Scenario**: Customers **C013–C016** share Device `D004`, Mobile `M002`, Bank `B007`, Address `A013`, Dealer `DL003`, and Guarantor `G005`.
- **Finding**: Individually each applicant appears low risk, but collectively they form a **CRITICAL** fraud cluster (risk score **91.5**).
- **Inspection**: Navigate to **Analyze** in the live web app, select any cluster member or dealer, and explore the interactive graph, risk breakdown, and evidence signals.

---

## 📂 Project Layout

```
swarm/
  README.md          # Project documentation & live deployment link
  frontend/          # React + Vite frontend (Vercel deployment)
  backend/           # FastAPI + SQLAlchemy + intelligence engine
  database/          # 31-table schema, seeds, queries, docs
  model/             # ML fraud detection models
```

---

## 🧪 Tests

- **Database**: 31-table schema verification + relationship graph integrity.
- **Backend**: 12 comprehensive unit & integration tests (health, CRUD, intelligence, ML features, clusters).
- **Frontend**: Clean production bundle build (`tsc -b && vite build`) and Vercel production deployment.
