from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date

class CustomerCreate(BaseModel):
    customer_ref: str = Field(pattern=r"^C[0-9]+$")
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    income_band: str = "UNKNOWN"
    customer_status: str = "ACTIVE"

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    customer_status: Optional[str] = None
    occupation: Optional[str] = None
    income_band: Optional[str] = None

class CustomerResponse(BaseModel):
    customer_id: UUID
    customer_ref: str
    full_name: str
    customer_status: str
    income_band: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    application_ref: str
    customer_id: UUID
    dealer_id: Optional[UUID] = None
    requested_amount: float = Field(gt=0)
    tenure_months: int = Field(ge=1, le=360)
    application_status: str = "SUBMITTED"

class ApplicationResponse(BaseModel):
    application_id: UUID
    application_ref: str
    customer_id: UUID
    dealer_id: Optional[UUID] = None
    requested_amount: float
    tenure_months: int
    application_status: str
    risk_score: Optional[float] = None
    fraud_score: Optional[float] = None
    class Config:
        from_attributes = True

class LoanResponse(BaseModel):
    loan_id: UUID
    application_id: UUID
    loan_account_ref: str
    sanctioned_amount: float
    loan_status: str
    class Config:
        from_attributes = True

class InvestigationCreate(BaseModel):
    alert_id: UUID
    investigator_ref: Optional[str] = None
    priority: str = "MEDIUM"
    notes: Optional[str] = None

class RiskResponse(BaseModel):
    entity_type: str
    entity_id: UUID
    risk_score: float
    fraud_probability: float
    risk_level: str
    model_version: str
    calculated_at: datetime
