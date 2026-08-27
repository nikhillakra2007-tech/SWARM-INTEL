"""All 31 SQLAlchemy models — mirrors database/schema/003_tables.sql"""
import uuid
from datetime import datetime, date
from sqlalchemy import (
    Enum,
    Column, String, Text, Integer, Numeric, Boolean, Date, DateTime, ForeignKey,
    UniqueConstraint, CheckConstraint, Index, func, JSON, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

# Use UUID type that works with both postgres and local reflection
UUID_PK = lambda: mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

# ---------- 1 customers ----------
class Customer(Base):
    __tablename__ = "customers"
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(30), nullable=True)
    pan_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    aadhaar_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    occupation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    income_band: Mapped[str] = mapped_column(String(20), nullable=False, default="UNKNOWN")
    customer_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 2 mobile_numbers
class MobileNumber(Base):
    __tablename__ = "mobile_numbers"
    mobile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mobile_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    country_code: Mapped[str] = mapped_column(String(5), nullable=False, default="+91")
    mobile_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 3 customer_mobile_links
class CustomerMobileLink(Base):
    __tablename__ = "customer_mobile_links"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    mobile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("mobile_numbers.mobile_id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False, default="PRIMARY")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("customer_id","mobile_id"),)

# 4 addresses
class Address(Base):
    __tablename__ = "addresses"
    address_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    address_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Numeric(9,6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9,6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 5 customer_address_links
class CustomerAddressLink(Base):
    __tablename__ = "customer_address_links"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    address_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("addresses.address_id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False, default="RESIDENTIAL")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("customer_id","address_id","relationship_type"),)

# 6 bank_accounts
class BankAccount(Base):
    __tablename__ = "bank_accounts"
    bank_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    bank_name: Mapped[str] = mapped_column(String(150), nullable=False)
    ifsc: Mapped[str | None] = mapped_column(String(11), nullable=True)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False, default="SAVINGS")
    account_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 7 customer_bank_links
class CustomerBankLink(Base):
    __tablename__ = "customer_bank_links"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    bank_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bank_accounts.bank_account_id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False, default="PRIMARY")
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("customer_id","bank_account_id"),)

# 8 devices
class Device(Base):
    __tablename__ = "devices"
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_fingerprint: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    device_type: Mapped[str] = mapped_column(String(20), nullable=False, default="MOBILE")
    os: Mapped[str | None] = mapped_column(String(100), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    device_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 9 customer_device_links
class CustomerDeviceLink(Base):
    __tablename__ = "customer_device_links"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    device_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.device_id"), nullable=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("customer_id","device_id"),)

# 10 ip_addresses
class IPAddress(Base):
    __tablename__ = "ip_addresses"
    ip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    ip_version: Mapped[str] = mapped_column(String(5), nullable=False, default="V4")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 11 dealers
class Dealer(Base):
    __tablename__ = "dealers"
    dealer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dealer_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    dealer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    dealer_type: Mapped[str] = mapped_column(String(20), nullable=False, default="DSA")
    address_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("addresses.address_id"), nullable=True)
    dealer_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    onboarding_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 12 dealer_customer_links
class DealerCustomerLink(Base):
    __tablename__ = "dealer_customer_links"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dealer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dealers.dealer_id"), nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    first_application_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_application_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    application_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    relationship_status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("dealer_id","customer_id"),)

# 13 loan_applications
class LoanApplication(Base):
    __tablename__ = "loan_applications"
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    dealer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("dealers.dealer_id"), nullable=True)
    requested_amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    application_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    application_status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUBMITTED")
    decision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    fraud_score: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 14 loans
class Loan(Base):
    __tablename__ = "loans"
    loan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_applications.application_id"), unique=True, nullable=False)
    loan_account_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    sanctioned_amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    disbursed_amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    interest_rate: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    disbursement_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    loan_status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDING_DISBURSEMENT")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 15 guarantors
class Guarantor(Base):
    __tablename__ = "guarantors"
    guarantor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guarantor_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    identity_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    mobile_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("mobile_numbers.mobile_id"), nullable=True)
    address_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("addresses.address_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 16 loan_guarantors
class LoanGuarantor(Base):
    __tablename__ = "loan_guarantors"
    link_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_applications.application_id"), nullable=False)
    guarantor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("guarantors.guarantor_id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False, default="GUARANTOR")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("application_id","guarantor_id"),)

# 17 payments
class Payment(Base):
    __tablename__ = "payments"
    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False, default="OTHER")
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUCCESS")
    days_past_due: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transaction_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    transaction_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 18 repayment_behaviour
class RepaymentBehaviour(Base):
    __tablename__ = "repayment_behaviour"
    behaviour_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), nullable=False)
    avg_payment_delay_days: Mapped[float] = mapped_column(Numeric(6,2), nullable=False, default=0)
    missed_payment_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    early_payment_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partial_payment_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bounce_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_velocity: Mapped[float | None] = mapped_column(Numeric(6,2), nullable=True)
    behaviour_score: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (UniqueConstraint("loan_id","calculated_at"),)

# 19 locations
class Location(Base):
    __tablename__ = "locations"
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude: Mapped[float | None] = mapped_column(Numeric(9,6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9,6), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 20 application_events
class ApplicationEvent(Base):
    __tablename__ = "application_events"
    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("loan_applications.application_id"), nullable=True)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=True)
    device_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("devices.device_id"), nullable=True)
    ip_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ip_addresses.ip_id"), nullable=True)
    location_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    _metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 21 entity_relationships — polymorphic core
class EntityRelationship(Base):
    __tablename__ = "entity_relationships"
    relationship_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    source_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    target_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(40), nullable=False)
    strength: Mapped[float] = mapped_column(Numeric(4,3), nullable=False, default=0.5)
    confidence: Mapped[float] = mapped_column(Numeric(4,3), nullable=False, default=0.5)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    _metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 22 fraud_signals — polymorphic
class FraudSignal(Base):
    __tablename__ = "fraud_signals"
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(Enum("LOW","MEDIUM","HIGH","CRITICAL", name="signal_severity", create_type=False), nullable=False, default="MEDIUM")
    score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(4,3), nullable=False, default=0.5)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 23 risk_scores — polymorphic append-only
class RiskScore(Base):
    __tablename__ = "risk_scores"
    risk_score_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    risk_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    fraud_probability: Mapped[float] = mapped_column(Numeric(5,4), nullable=False)
    risk_level: Mapped[str] = mapped_column(Enum("LOW","MEDIUM","HIGH","CRITICAL", name="risk_level", create_type=False), nullable=False)
    model_version: Mapped[str] = mapped_column(String(30), nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    feature_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 24 fraud_clusters
class FraudCluster(Base):
    __tablename__ = "fraud_clusters"
    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    cluster_type: Mapped[str] = mapped_column(Enum("DEVICE_CLUSTER","MOBILE_CLUSTER","BANK_ACCOUNT_CLUSTER","DEALER_CLUSTER","MIXED_ENTITY_CLUSTER","BEHAVIOURAL_CLUSTER","OTHER", name="cluster_type", create_type=False), nullable=False, default="MIXED_ENTITY_CLUSTER")
    risk_score: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    member_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cluster_status: Mapped[str] = mapped_column(Enum("ACTIVE","UNDER_REVIEW","CONFIRMED_FRAUD","FALSE_POSITIVE","ARCHIVED", name="cluster_status", create_type=False), nullable=False, default="ACTIVE")
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    _metadata: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))

# 25 fraud_cluster_members — polymorphic
class FraudClusterMember(Base):
    __tablename__ = "fraud_cluster_members"
    member_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fraud_clusters.cluster_id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    membership_score: Mapped[float] = mapped_column(Numeric(4,3), nullable=False, default=0.5)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

# 26 fraud_alerts — polymorphic + optional cluster FK
class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    alert_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_ref: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    cluster_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("fraud_clusters.cluster_id"), nullable=True)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(Enum("LOW","MEDIUM","HIGH","CRITICAL", name="alert_severity", create_type=False), nullable=False, default="MEDIUM")
    risk_score: Mapped[float | None] = mapped_column(Numeric(5,2), nullable=True)
    alert_status: Mapped[str] = mapped_column(Enum("OPEN","ACKNOWLEDGED","IN_INVESTIGATION","RESOLVED","DISMISSED","ESCALATED", name="alert_status", create_type=False), nullable=False, default="OPEN")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 27 investigations
class Investigation(Base):
    __tablename__ = "investigations"
    investigation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fraud_alerts.alert_id"), nullable=False)
    investigator_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    investigation_status: Mapped[str] = mapped_column(Enum("OPEN","IN_PROGRESS","ON_HOLD","CLOSED","ESCALATED", name="investigation_status", create_type=False), nullable=False, default="OPEN")
    priority: Mapped[str] = mapped_column(Enum("LOW","MEDIUM","HIGH","URGENT", name="investigation_priority", create_type=False), nullable=False, default="MEDIUM")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# 28 investigation_actions
class InvestigationAction(Base):
    __tablename__ = "investigation_actions"
    action_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("investigations.investigation_id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(40), nullable=False)
    performed_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 29 model_versions
class ModelVersion(Base):
    __tablename__ = "model_versions"
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)
    training_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    performance_metrics: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    model_status: Mapped[str] = mapped_column(Enum("TRAINING","EVALUATING","ACTIVE","RETIRED","FAILED", name="model_status", create_type=False), nullable=False, default="TRAINING")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 30 predictions — polymorphic
class Prediction(Base):
    __tablename__ = "predictions"
    prediction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("model_versions.model_id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    prediction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prediction_score: Mapped[float] = mapped_column(Numeric(6,4), nullable=False)
    prediction_label: Mapped[str | None] = mapped_column(String(30), nullable=True)
    feature_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    predicted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 31 audit_logs
class AuditLog(Base):
    __tablename__ = "audit_logs"
    audit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    old_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
