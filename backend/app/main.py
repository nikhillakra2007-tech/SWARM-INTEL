from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import get_settings
from app.database import get_db, check_db
from sqlalchemy.orm import Session

settings = get_settings()

app = FastAPI(title="Swarm Intelligence Lending Network", version="0.1.0", description="AI-driven lending fraud intelligence — collective network detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from app.api.customers import router as customers_r
from app.api.applications import router as apps_r
from app.api.loans import router as loans_r
from app.api.devices import router as devices_r
from app.api.dealers import router as dealers_r
from app.api.relationships import router as rels_r
from app.api.network import router as network_r
from app.api.fraud import router as fraud_r
from app.api.risk import router as risk_r
from app.api.clusters import router as clusters_r
from app.api.alerts import router as alerts_r
from app.api.investigations import router as invs_r
from app.api.predictions import router as preds_r
from app.api.intelligence import router as intel_r

app.include_router(customers_r)
app.include_router(apps_r)
app.include_router(loans_r)
app.include_router(devices_r)
app.include_router(dealers_r)
app.include_router(rels_r)
app.include_router(network_r)
app.include_router(fraud_r)
app.include_router(risk_r)
app.include_router(clusters_r)
app.include_router(alerts_r)
app.include_router(invs_r)
app.include_router(preds_r)
app.include_router(intel_r)

@app.get("/health", summary="Health check", tags=["health"])
def health(db: Session = Depends(get_db)):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    return {"status": "healthy" if db_ok else "degraded", "database": "connected" if db_ok else "disconnected", "env": settings.APP_ENV}

@app.get("/", summary="Root")
def root():
    return {"name": "Swarm Intelligence Lending Network", "docs": "/docs", "health": "/health"}

# Optional: ensure model exists on startup
@app.on_event("startup")
def startup_train():
    try:
        from app.database import SessionLocal
        from app.ml.training.pipeline import train_from_db
        from pathlib import Path
        model_path = Path(__file__).parent / "ml" / "models" / "fraud_baseline.pkl"
        if not model_path.exists():
            db = SessionLocal()
            try:
                train_from_db(db)
            finally:
                db.close()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("startup train failed: %s", e)
