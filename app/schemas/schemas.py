from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: str
    role: str
    tenant_id: str
    tenant_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterTenantRequest(BaseModel):
    tenant_name: str
    tenant_slug: str
    admin_email: str
    admin_password: str
    admin_name: str
    tier: str = "GROWTH"

class PropertyCreate(BaseModel):
    title: str
    category: str
    city: str = "Hyderabad"
    neighborhood: str
    address: Optional[str] = None
    asking_price: float
    currency: str = "INR"
    size_sqft: float
    unit: str = "sq_ft"
    description: Optional[str] = None
    listing_source: str = "Manual Entry / Listing Portal"
    original_url: Optional[str] = None
    availability_status: str = "AVAILABLE"
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    legal_verification_status: str = "PENDING_DOCUMENT_CHECK"
    investment_notes: Optional[str] = None

class PropertyResponse(PropertyCreate):
    id: str
    tenant_id: str
    price_per_sqft: Optional[float]
    confidence_label: str
    is_duplicate: bool
    duplicate_of_id: Optional[str]
    source_date: datetime
    last_verified_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class LeadCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    preferred_channel: str = "EMAIL"
    consent_status: str = "CONSENT_GRANTED"
    consent_source: str = "Direct Inquiry Form"
    property_category: str = "Commercial"
    preferred_locations: str = "HITEC City, Gachibowli"
    budget_min: float = 10000000.0
    budget_max: float = 50000000.0
    currency: str = "INR"
    purpose: str = "Investment"
    purchase_timeframe: str = "1 to 3 months"
    status: str = "NEW"

class LeadResponse(LeadCreate):
    id: str
    tenant_id: str
    qualification_score: float
    qualification_reason: Optional[str]
    missing_information: Optional[str]
    recommended_action: Optional[str]
    last_interaction_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    lead_id: str
    title: str
    appointment_type: str = "Property Visit"
    start_time: datetime
    end_time: datetime
    timezone: str = "Asia/Kolkata"
    location_or_link: str = "Site Visit, Hyderabad"
    notes: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: str
    tenant_id: str
    status: str
    calendar_event_id: Optional[str]
    reminder_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True

class InvestorReportCreate(BaseModel):
    title: str
    property_id: Optional[str] = None
    client_name: str
    target_budget: float
    property_type: str = "Commercial Office"
    preferred_locations: str = "HITEC City, Hyderabad"
    asking_price: float
    estimated_rental_yield: float = 7.5
    gross_yield: float = 8.2
    cap_rate: float = 6.8
    monthly_expenses: float = 25000.0
    vacancy_rate_pct: float = 5.0
    maintenance_reserve_pct: float = 3.0
    risks_and_caveats: str
    legal_due_diligence_checklist: str
    executive_summary: str

class InvestorReportResponse(InvestorReportCreate):
    id: str
    tenant_id: str
    pdf_path: Optional[str]
    xlsx_path: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrchestratorCommandRequest(BaseModel):
    command: str

class AgentTaskResponse(BaseModel):
    id: str
    tenant_id: str
    agent_name: str
    command: str
    status: str
    retry_count: int
    cost_estimate_usd: float
    output_payload_json: Optional[str]
    error_details: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ApprovalDecisionRequest(BaseModel):
    decision: str  # APPROVED or REJECTED
    comment: Optional[str] = None

class ApprovalResponse(BaseModel):
    id: str
    tenant_id: str
    task_id: Optional[str]
    action_type: str
    description: str
    status: str
    requested_by_agent: str
    reviewed_at: Optional[datetime]
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
