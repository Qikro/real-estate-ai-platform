from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(120), nullable=False)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    tier = Column(String(50), default="GROWTH")  # STARTER ($299), GROWTH ($999), INVESTOR_OPS ($1999)
    status = Column(String(30), default="ACTIVE")
    monthly_fee = Column(Float, default=999.0)
    currency = Column(String(10), default="USD")
    contact_email = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=utc_now)

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    properties = relationship("PropertyListing", back_populates="tenant", cascade="all, delete-orphan")
    leads = relationship("BuyerLead", back_populates="tenant", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="tenant", cascade="all, delete-orphan")
    reports = relationship("InvestorReport", back_populates="tenant", cascade="all, delete-orphan")
    tasks = relationship("AgentTask", back_populates="tenant", cascade="all, delete-orphan")
    approvals = relationship("ApprovalRequest", back_populates="tenant", cascade="all, delete-orphan")
    transactions = relationship("FinancialTransaction", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(30), default="AGENT")  # SUPER_ADMIN, BROKER_ADMIN, AGENT, INVESTOR
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    tenant = relationship("Tenant", back_populates="users")


class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # Commercial, Residential, Industrial, Plot, Office, Warehouse
    city = Column(String(100), default="Hyderabad", index=True)
    neighborhood = Column(String(100), nullable=False, index=True)  # HITEC City, Gachibowli, Kokapet, etc.
    address = Column(String(255), nullable=True)
    asking_price = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    size_sqft = Column(Float, nullable=False)
    unit = Column(String(30), default="sq_ft")
    price_per_sqft = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    listing_source = Column(String(100), default="Authorized Developer Feed")
    original_url = Column(String(500), nullable=True)
    source_date = Column(DateTime, default=utc_now)
    last_verified_date = Column(DateTime, default=utc_now)
    availability_status = Column(String(30), default="AVAILABLE")  # AVAILABLE, UNDER_OFFER, SOLD
    contact_name = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(120), nullable=True)
    legal_verification_status = Column(String(50), default="PENDING_DOCUMENT_CHECK")
    confidence_label = Column(String(40), default="VERIFIED_FROM_SOURCE")
    # VERIFIED_FROM_SOURCE, PARTIALLY_VERIFIED, UNVERIFIED, OUTDATED, CONFLICTING_SOURCES
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(String(36), nullable=True)
    investment_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    tenant = relationship("Tenant", back_populates="properties")


class BuyerLead(Base):
    __tablename__ = "buyer_leads"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    preferred_channel = Column(String(30), default="EMAIL")  # EMAIL, PHONE, WHATSAPP
    consent_status = Column(String(40), default="CONSENT_GRANTED")  # CONSENT_GRANTED, PENDING, REVOKED
    consent_source = Column(String(100), default="Website Inquiry Form")
    consent_timestamp = Column(DateTime, default=utc_now)
    property_category = Column(String(50), default="Commercial")
    preferred_locations = Column(String(255), default="HITEC City, Gachibowli")
    budget_min = Column(Float, default=10000000.0)  # INR 1 Crore
    budget_max = Column(Float, default=50000000.0)  # INR 5 Crore
    currency = Column(String(10), default="INR")
    purpose = Column(String(50), default="Investment")  # Investment, Self-Use, Expansion
    purchase_timeframe = Column(String(50), default="1 to 3 months")
    assigned_agent_id = Column(String(36), nullable=True)
    status = Column(String(40), default="NEW")
    # NEW, CONTACT_PERMISSION_PENDING, CONTACTED, INFORMATION_PENDING, QUALIFIED, NOT_QUALIFIED, FOLLOW_UP, DO_NOT_CONTACT
    qualification_score = Column(Float, default=0.0)
    qualification_reason = Column(Text, nullable=True)
    missing_information = Column(Text, nullable=True)
    recommended_action = Column(String(255), default="Schedule preliminary discovery call")
    last_interaction_date = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    tenant = relationship("Tenant", back_populates="leads")
    appointments = relationship("Appointment", back_populates="lead", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    lead_id = Column(String(36), ForeignKey("buyer_leads.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    appointment_type = Column(String(50), default="Property Visit")  # Property Visit, Investor Consultation, Buyer Call, Broker Meeting
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    timezone = Column(String(50), default="Asia/Kolkata")
    location_or_link = Column(String(255), default="On-site / Google Meet")
    status = Column(String(30), default="SCHEDULED")  # PROPOSED, SCHEDULED, COMPLETED, CANCELLED, RESCHEDULED
    calendar_event_id = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    broker_id = Column(String(36), nullable=True)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    tenant = relationship("Tenant", back_populates="appointments")
    lead = relationship("BuyerLead", back_populates="appointments")


class InvestorReport(Base):
    __tablename__ = "investor_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    property_id = Column(String(36), ForeignKey("property_listings.id", ondelete="SET NULL"), nullable=True)
    client_name = Column(String(100), nullable=False)
    target_budget = Column(Float, nullable=False)
    property_type = Column(String(50), default="Commercial Office")
    preferred_locations = Column(String(255), default="HITEC City, Hyderabad")
    executive_summary = Column(Text, nullable=False)
    asking_price = Column(Float, nullable=False)
    estimated_rental_yield = Column(Float, default=7.5)  # Percentage %
    gross_yield = Column(Float, default=8.2)
    cap_rate = Column(Float, default=6.8)
    monthly_expenses = Column(Float, default=25000.0)
    vacancy_rate_pct = Column(Float, default=5.0)
    maintenance_reserve_pct = Column(Float, default=3.0)
    risks_and_caveats = Column(Text, nullable=False)
    legal_due_diligence_checklist = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=True)
    pdf_path = Column(String(255), nullable=True)
    xlsx_path = Column(String(255), nullable=True)
    status = Column(String(30), default="READY")
    created_at = Column(DateTime, default=utc_now)

    tenant = relationship("Tenant", back_populates="reports")


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name = Column(String(60), nullable=False, index=True)
    command = Column(String(255), nullable=False)
    input_payload_json = Column(Text, nullable=True)
    output_payload_json = Column(Text, nullable=True)
    status = Column(String(30), default="PENDING", index=True)  # PENDING, RUNNING, COMPLETED, FAILED, WAITING_APPROVAL
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    error_details = Column(Text, nullable=True)
    cost_estimate_usd = Column(Float, default=0.01)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    tenant = relationship("Tenant", back_populates="tasks")


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(String(36), nullable=True)
    action_type = Column(String(80), nullable=False)  # OUTBOUND_COMMUNICATION, REPORT_DISPATCH, PRICE_CHANGE, DELETE_RECORD
    description = Column(Text, nullable=False)
    proposed_payload_json = Column(Text, nullable=True)
    status = Column(String(30), default="PENDING", index=True)  # PENDING, APPROVED, REJECTED
    requested_by_agent = Column(String(60), default="Quality & Compliance Agent")
    reviewed_by_user_id = Column(String(36), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    tenant = relationship("Tenant", back_populates="approvals")


class SalesProspect(Base):
    __tablename__ = "sales_prospects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    business_name = Column(String(150), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=True)
    category = Column(String(60), default="Real Estate Brokerage")  # Brokerage, Developer, Investment Firm, Property Consultant
    city = Column(String(100), default="Hyderabad")
    state = Column(String(100), default="Telangana")
    website = Column(String(200), nullable=True)
    proposal_draft = Column(Text, nullable=True)
    status = Column(String(40), default="DISCOVERED")  # DISCOVERED, PROPOSAL_DRAFTED, OUTREACH_PENDING_APPROVAL, ENGAGED, WON, LOST
    estimated_value = Column(Float, default=999.0)
    assigned_sales_rep = Column(String(100), default="Sales & Growth Agent")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    package_name = Column(String(60), default="REAL ESTATE GROWTH")
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    billing_interval = Column(String(20), default="MONTHLY")
    status = Column(String(30), default="PAID")  # PAID, PENDING, REFUNDED
    payment_provider = Column(String(50), default="Mock / Stripe / Razorpay")
    invoice_url = Column(String(255), nullable=True)
    ai_cost_usd = Column(Float, default=12.45)
    infrastructure_cost_usd = Column(Float, default=4.50)
    gross_margin_usd = Column(Float, default=982.05)
    transaction_date = Column(DateTime, default=utc_now)

    tenant = relationship("Tenant", back_populates="transactions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(60), nullable=False)
    entity_id = Column(String(36), nullable=True)
    change_details_json = Column(Text, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    created_at = Column(DateTime, default=utc_now)

    tenant = relationship("Tenant", back_populates="audit_logs")
