import pytest
import uuid
from datetime import datetime, timezone, timedelta
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.entities import (
    Tenant, User, PropertyListing, BuyerLead, Appointment,
    InvestorReport, ApprovalRequest, FinancialTransaction
)
from app.agents.orchestrator import orchestrator
from app.services.dedup_service import check_duplicate_property

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_user_authentication():
    pwd = "SecureBrokerPassword2026!"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

    token = create_access_token({"sub": "user-123", "role": "BROKER_ADMIN"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user-123"
    assert payload["role"] == "BROKER_ADMIN"

def test_tenant_isolation(db_session):
    u_id = uuid.uuid4().hex[:6]
    # Create two separate tenants with unique slugs
    t1 = Tenant(name="Tenant Alpha", slug=f"tenant-alpha-{u_id}", tier="GROWTH", contact_email=f"alpha-{u_id}@domain.com")
    t2 = Tenant(name="Tenant Beta", slug=f"tenant-beta-{u_id}", tier="STARTER", contact_email=f"beta-{u_id}@domain.com")
    db_session.add_all([t1, t2])
    db_session.commit()

    # Add property to tenant 1
    p1 = PropertyListing(
        tenant_id=t1.id,
        title=f"Alpha Tech Hub {u_id}",
        category="Commercial Office",
        neighborhood="HITEC City",
        asking_price=50000000.0,
        size_sqft=4000.0
    )
    db_session.add(p1)
    db_session.commit()

    # Query properties for Tenant 2 - must be strictly 0
    t2_props = db_session.query(PropertyListing).filter(PropertyListing.tenant_id == t2.id).all()
    assert len(t2_props) == 0

    t1_props = db_session.query(PropertyListing).filter(PropertyListing.tenant_id == t1.id).all()
    assert len(t1_props) >= 1

def test_property_deduplication(db_session):
    t = db_session.query(Tenant).first()
    u_id = uuid.uuid4().hex[:6]
    title = f"Signature Commercial Space {u_id}"
    neighborhood = f"FinDistrict_{u_id}"
    price = 60000000.0
    size = 5000.0
    url = f"https://hyderabad-realty.in/listing/sig-space-{u_id}"

    # Insert initial
    p = PropertyListing(
        tenant_id=t.id,
        title=title,
        neighborhood=neighborhood,
        category="Commercial Office",
        asking_price=price,
        size_sqft=size,
        original_url=url
    )
    db_session.add(p)
    db_session.commit()

    # Deduplication test 1: Exact URL match
    is_dup_url, dup_id_url = check_duplicate_property(db_session, t.id, "Different Title", "Other Loc", 1000.0, 100.0, url)
    assert is_dup_url is True
    assert dup_id_url == p.id

    # Deduplication test 2: Heuristic matching (same neighborhood, price within 1%, size within 1%)
    is_dup_attr, dup_id_attr = check_duplicate_property(db_session, t.id, title, neighborhood, price * 1.005, size * 0.998)
    assert is_dup_attr is True
    assert dup_id_attr == p.id

    # Non-duplicate test: different neighborhood & different price
    is_dup_diff, _ = check_duplicate_property(db_session, t.id, "Warehouse Facility", f"Other_{u_id}", 30000000.0, 12000.0)
    assert is_dup_diff is False

def test_lead_qualification_scoring(db_session):
    t = db_session.query(Tenant).first()
    u_id = uuid.uuid4().hex[:6]

    # High-intent lead with full details
    lead_high = BuyerLead(
        tenant_id=t.id,
        full_name=f"Rajiv Malhotra {u_id}",
        email=f"rajiv.{u_id}@investments.in",
        phone="+91 99887 66554",
        consent_status="CONSENT_GRANTED",
        property_category="Commercial Office",
        preferred_locations="HITEC City",
        budget_min=30000000.0,
        budget_max=60000000.0,
        purchase_timeframe="1 month",
        status="NEW"
    )
    db_session.add(lead_high)
    db_session.commit()

    res = orchestrator.departments["buyer_qualification"].execute(
        tenant_id=t.id,
        command="Qualify lead",
        payload={"lead_id": lead_high.id},
        db=db_session
    )
    db_session.refresh(lead_high)

    assert lead_high.qualification_score >= 75.0
    assert lead_high.status == "QUALIFIED"
    assert "HITEC City" in lead_high.qualification_reason

def test_consent_and_opt_out_enforcement(db_session):
    t = db_session.query(Tenant).first()
    u_id = uuid.uuid4().hex[:6]

    # Opted-out lead
    lead_opt_out = {
        "full_name": f"Spam Candidate {u_id}",
        "email": f"optout_{u_id}@candidate.in",
        "phone": "+91 90000 99999",
        "consent_status": "REVOKED",
        "status": "DO_NOT_CONTACT"
    }

    res = orchestrator.departments["buyer_lead"].execute(
        tenant_id=t.id,
        command="Ingest lead",
        payload={"leads": [lead_opt_out]},
        db=db_session
    )

    assert res["skipped_count"] >= 1
    # Ensure not inserted
    db_lead = db_session.query(BuyerLead).filter(BuyerLead.email == f"optout_{u_id}@candidate.in").first()
    assert db_lead is None

def test_appointment_conflict_prevention(db_session):
    t = db_session.query(Tenant).first()
    lead = db_session.query(BuyerLead).filter(BuyerLead.tenant_id == t.id).first()
    u_id = uuid.uuid4().hex[:6]
    day_offset = 100 + (int(u_id, 16) % 500)

    # Schedule appointment slot 1 with unique future date
    t1_start = datetime.now(timezone.utc) + timedelta(days=day_offset, hours=2)
    res1 = orchestrator.departments["appointment_booking"].execute(
        tenant_id=t.id,
        command="Schedule 1",
        payload={
            "lead_id": lead.id,
            "title": f"Site Inspection 1 {u_id}",
            "start_time": t1_start.isoformat(),
            "duration_minutes": 60
        },
        db=db_session
    )
    assert res1["status"] == "SUCCESS"

    # Attempt to schedule overlapping appointment in same window
    t2_start = t1_start + timedelta(minutes=30)
    res2 = orchestrator.departments["appointment_booking"].execute(
        tenant_id=t.id,
        command="Schedule 2 - Overlap",
        payload={
            "lead_id": lead.id,
            "title": f"Site Inspection 2 - Overlap {u_id}",
            "start_time": t2_start.isoformat(),
            "duration_minutes": 60
        },
        db=db_session
    )
    assert res2["status"] == "CONFLICT_DETECTED"
    assert "conflicts with existing appointment" in res2["message"]

def test_investor_report_underwriting_calculations(db_session):
    t = db_session.query(Tenant).first()
    prop = db_session.query(PropertyListing).filter(PropertyListing.tenant_id == t.id).first()

    res = orchestrator.departments["investor_reporting"].execute(
        tenant_id=t.id,
        command="Underwrite asset",
        payload={
            "property_id": prop.id,
            "client_name": "Sovereign Real Estate Fund"
        },
        db=db_session
    )
    assert res["status"] == "SUCCESS"
    assert "cap_rate" in res
    assert "gross_yield" in res
    assert res["pdf_download"] is not None
    assert res["xlsx_download"] is not None

def test_master_orchestrator_natural_language_dispatch(db_session):
    t = db_session.query(Tenant).first()
    u_id = uuid.uuid4().hex[:6]

    # NL command: "Find verified commercial properties in Hyderabad"
    res = orchestrator.execute(
        tenant_id=t.id,
        command=f"Find verified commercial properties in Hyderabad {u_id}",
        payload={},
        db=db_session
    )
    assert res["status"] == "SUCCESS"
    assert res["target_department"] == "property_research"

def test_compliance_approval_gate_workflow(db_session):
    t = db_session.query(Tenant).first()

    # Trigger action requiring approval
    res = orchestrator.departments["compliance_qa"].execute(
        tenant_id=t.id,
        command="Outbound Proposal Gate",
        payload={
            "action": "REQUEST_APPROVAL",
            "action_type": "OUTBOUND_OFFER_DISPATCH",
            "description": "Send formal binding acquisition offer to commercial landlord",
            "proposed_payload": {"offer_inr": 45000000.0}
        },
        db=db_session
    )

    assert res["status"] == "APPROVAL_REQUIRED"
    approval_id = res["approval_id"]

    # Verify pending state in database
    approval = db_session.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
    assert approval is not None
    assert approval.status == "PENDING"

    # Human broker review: APPROVE
    approval.status = "APPROVED"
    approval.comment = "Commercial terms verified by principal broker"
    db_session.commit()

    db_session.refresh(approval)
    assert approval.status == "APPROVED"

def test_financial_revenue_unit_economics(db_session):
    t = db_session.query(Tenant).first()

    res = orchestrator.departments["finance_monitor"].execute(
        tenant_id=t.id,
        command="Compute unit economics",
        payload={},
        db=db_session
    )
    assert res["status"] == "SUCCESS"
    metrics = res["metrics"]
    assert metrics["monthly_recurring_revenue_usd"] >= 1999.0
    assert metrics["target_daily_revenue_usd"] == 1000.0
    assert metrics["estimated_gross_margin_pct"] > 80.0
