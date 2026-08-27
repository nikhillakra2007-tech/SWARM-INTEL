from pydantic import BaseModel
from typing import Optional, Any, List
from uuid import UUID

class IndividualRisk(BaseModel):
    score: float
    level: str
    top_signals: List[dict] = []

class NetworkRisk(BaseModel):
    score: float
    level: str
    degree: int
    high_risk_neighbors: int

class MLPrediction(BaseModel):
    fraud_probability: float
    prediction: str
    model_version: str
    threshold: float

class CollectiveRisk(BaseModel):
    score: float
    level: str
    confidence: float
    weights: dict

class AnalysisResponse(BaseModel):
    entity_type: str
    entity_id: str
    individual_risk: IndividualRisk
    network_risk: NetworkRisk
    ml_prediction: MLPrediction
    collective_risk: CollectiveRisk
    signals: List[dict]
    anomalies: dict
    temporal: dict
    network: dict
    cluster: Optional[dict] = None
    evidence: List[str]
    alert: Optional[dict] = None
    feature_schema: List[str]
