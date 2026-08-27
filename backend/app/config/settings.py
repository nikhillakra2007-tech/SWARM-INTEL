from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/swarm_lending"
    APP_ENV: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    MODEL_PATH: str = "app/ml/models/fraud_baseline.pkl"
    MODEL_VERSION: str = "v2.1.0"
    RISK_THRESHOLD: float = 60.0
    ANOMALY_THRESHOLD: float = 0.7
    CLUSTER_THRESHOLD: int = 3
    MAX_GRAPH_DEPTH: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
