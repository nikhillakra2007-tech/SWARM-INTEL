from sqlalchemy.orm import Session
from uuid import UUID
from app.models import (
    Customer, LoanApplication, Loan, Device, Dealer, EntityRelationship,
    FraudSignal, RiskScore, FraudCluster, FraudClusterMember, FraudAlert,
    Investigation, Prediction, ModelVersion
)

ALLOWED_ENTITY_TYPES = {"CUSTOMER","MOBILE","DEVICE","BANK_ACCOUNT","ADDRESS","DEALER","GUARANTOR","IP","LOAN","APPLICATION","LOCATION","CLUSTER"}

def list_customers(db: Session, skip=0, limit=20):
    q = db.query(Customer)
    total = q.count()
    return q.offset(skip).limit(limit).all(), total

def get_customer(db: Session, cid: UUID):
    return db.query(Customer).filter(Customer.customer_id == cid).first()

def get_customer_by_ref(db: Session, ref: str):
    return db.query(Customer).filter(Customer.customer_ref == ref).first()
