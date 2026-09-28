from datetime import datetime, timezone, timedelta
import json
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.entities import (
    Tenant, User, PropertyListing, BuyerLead, Appointment,
    InvestorReport, ApprovalRequest, SalesProspect, FinancialTransaction, AuditLog, AgentTask
)
from app.agents.property_research import HYDERABAD_INVENTORY_FEED
from app.agents.buyer_lead import AUTHORIZED_INSTITUTIONAL_LEADS
from app.agents.sales_growth import TARGET_HYDERABAD_PROSPECTS
from app.services.pdf_generator import generate_pdf_report
from app.services.excel_generator import generate_excel_report

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if tenant exists
    tenant = db.query(Tenant).filter(Tenant.slug == "apex-realty-hyderabad").first()
    if not tenant:
        print("[*] Creating primary tenant workspace: Apex Realty & Capital Advisory (Hyderabad)")
        tenant = Tenant(
            name="Apex Realty & Capital Advisory",
            slug="apex-realty-hyderabad",
            tier="INVESTOR_OPS",
            status="ACTIVE",
            monthly_fee=1999.0,
            currency="USD",
            contact_email="operations@apexrealty.co.in"
        )
        db.add(tenant)
        db.flush()

        # Create Admin Users
        admin_user_estate = User(
            tenant_id=tenant.id,
            email="admin@estate.ai",
            hashed_password=get_password_hash("Admin@123456"),
            full_name="Quill Operations Lead",
            role="SUPER_ADMIN"
        )
        admin_user_apex = User(
            tenant_id=tenant.id,
            email="operations@apexrealty.co.in",
            hashed_password=get_password_hash("Admin@123456"),
            full_name="Apex Principal Advisory Desk",
            role="SUPER_ADMIN"
        )
        broker_user = User(
            tenant_id=tenant.id,
            email="broker@apexrealty.co.in",
            hashed_password=get_password_hash("Broker@123456"),
            full_name="Rajesh Varma",
            role="BROKER_ADMIN"
        )
        db.add(admin_user_estate)
        db.add(admin_user_apex)
        db.add(broker_user)
        db.flush()

        # Seed Verified Properties
        print("[*] Seeding verified Hyderabad commercial & investment inventory...")
        created_props = []
        for item in HYDERABAD_INVENTORY_FEED:
            price = item["asking_price"]
            size = item["size_sqft"]
            prop = PropertyListing(
                tenant_id=tenant.id,
                title=item["title"],
                category=item["category"],
                city=item.get("city", "Hyderabad"),
                neighborhood=item["neighborhood"],
                address=item["address"],
                asking_price=price,
                currency="INR",
                size_sqft=size,
                unit="sq_ft",
                price_per_sqft=round(price / size, 2),
                description=item.get("investment_notes", f"Verified Grade-A asset in {item['neighborhood']}."),
                listing_source=item["listing_source"],
                original_url=item["original_url"],
                contact_name=item["contact_name"],
                contact_phone=item["contact_phone"],
                contact_email=item["contact_email"],
                legal_verification_status=item["legal_verification_status"],
                confidence_label=item["confidence_label"],
                investment_notes=item["investment_notes"]
            )
            db.add(prop)
            created_props.append(prop)
        db.flush()

        # Seed Leads
        print("[*] Seeding opt-in buyer leads...")
        created_leads = []
        for lead_item in AUTHORIZED_INSTITUTIONAL_LEADS:
            lead = BuyerLead(
                tenant_id=tenant.id,
                full_name=lead_item["full_name"],
                email=lead_item["email"],
                phone=lead_item["phone"],
                preferred_channel=lead_item["preferred_channel"],
                consent_status=lead_item["consent_status"],
                consent_source=lead_item["consent_source"],
                property_category=lead_item["property_category"],
                preferred_locations=lead_item["preferred_locations"],
                budget_min=lead_item["budget_min"],
                budget_max=lead_item["budget_max"],
                currency="INR",
                purpose=lead_item["purpose"],
                purchase_timeframe=lead_item["purchase_timeframe"],
                status="QUALIFIED",
                qualification_score=88.0,
                qualification_reason="Verified budget readiness, clear acquisition timeline, and written inquiry consent.",
                recommended_action="Schedule asset tour in HITEC City / Financial District"
            )
            db.add(lead)
            created_leads.append(lead)
        db.flush()

        # Seed Appointments
        print("[*] Seeding verified appointments...")
        appt_time = datetime.now(timezone.utc) + timedelta(days=1, hours=4)
        appt = Appointment(
            tenant_id=tenant.id,
            lead_id=created_leads[0].id,
            title=f"Site Inspection: {created_props[0].title}",
            appointment_type="Property Visit",
            start_time=appt_time,
            end_time=appt_time + timedelta(hours=1),
            timezone="Asia/Kolkata",
            location_or_link="Mindspace Madhapur Commercial Corridor, Hyderabad",
            status="SCHEDULED",
            notes="Client evaluating 18,500 sqft pre-leased office asset with 8.1% gross yield.",
            reminder_sent=True
        )
        db.add(appt)

        # Seed Sample Report with PDF & Excel
        print("[*] Generating baseline investor report...")
        report_data = {
            "title": f"Investment Memorandum: {created_props[0].title}",
            "client_name": created_leads[0].full_name,
            "preferred_locations": "HITEC City, Hyderabad",
            "target_budget": 200000000.0,
            "asking_price": created_props[0].asking_price,
            "gross_yield": 8.1,
            "cap_rate": 7.4,
            "monthly_expenses": 95000.0,
            "vacancy_rate_pct": 5.0,
            "maintenance_reserve_pct": 3.0,
            "executive_summary": "Institutional underwriting model for Grade-A Mindspace IT Park commercial asset pre-leased to Fortune 500 GCC.",
            "risks_and_caveats": "Tenant contractual escalation 15% every 36 months; lock-in period through Q3 2029.",
            "legal_due_diligence_checklist": "- 30-year TS-RERA Encumbrance Certificate Cleared\\n- HMDA Sanction Plan Verified\\n- RERA Certification P02400004189 Active"
        }
        pdf_f = f"report_{tenant.id[:8]}_benchmark.pdf"
        xlsx_f = f"model_{tenant.id[:8]}_benchmark.xlsx"
        pdf_path = generate_pdf_report(report_data, pdf_f)
        xlsx_path = generate_excel_report(report_data, xlsx_f)

        report = InvestorReport(
            tenant_id=tenant.id,
            title=report_data["title"],
            property_id=created_props[0].id,
            client_name=created_leads[0].full_name,
            target_budget=200000000.0,
            property_type=created_props[0].category,
            preferred_locations="HITEC City, Hyderabad",
            executive_summary=report_data["executive_summary"],
            asking_price=created_props[0].asking_price,
            estimated_rental_yield=8.1,
            gross_yield=8.1,
            cap_rate=7.4,
            monthly_expenses=95000.0,
            vacancy_rate_pct=5.0,
            maintenance_reserve_pct=3.0,
            risks_and_caveats=report_data["risks_and_caveats"],
            legal_due_diligence_checklist=report_data["legal_due_diligence_checklist"],
            sources_json=json.dumps([{"source": created_props[0].listing_source, "url": created_props[0].original_url}]),
            pdf_path=pdf_path,
            xlsx_path=xlsx_path,
            status="READY"
        )
        db.add(report)

        # Seed Sales Prospects & Pending Approvals
        print("[*] Seeding sales prospects and approval gates...")
        for p in TARGET_HYDERABAD_PROSPECTS:
            prospect = SalesProspect(
                tenant_id=tenant.id,
                business_name=p["business_name"],
                contact_person=p["contact_person"],
                email=p["email"],
                phone=p["phone"],
                website=p["website"],
                category=p["category"],
                city=p["city"],
                state=p["state"],
                estimated_value=p["estimated_value"],
                status="PROPOSAL_DRAFTED",
                notes="Enterprise B2B target identified in West Hyderabad commercial corridor."
            )
            db.add(prospect)

            approval = ApprovalRequest(
                tenant_id=tenant.id,
                action_type="OUTBOUND_B2B_SALES_PROPOSAL",
                description=f"Approve sending institutional AI platform proposal to {p['business_name']} ({p['contact_person']})",
                requested_by_agent="Sales & Business Growth Agent",
                proposed_payload_json=json.dumps({"email": p["email"], "business": p["business_name"]}),
                status="PENDING"
            )
            db.add(approval)

        # Seed Financial Transactions
        print("[*] Seeding financial telemetry...")
        db.add(FinancialTransaction(
            tenant_id=tenant.id,
            package_name="INVESTOR_OPS_ENTERPRISE",
            amount=1999.0,
            currency="USD",
            billing_interval="MONTHLY",
            status="PAID",
            payment_provider="Razorpay / Stripe Connect",
            ai_cost_usd=28.50,
            infrastructure_cost_usd=12.00,
            gross_margin_usd=1958.50
        ))

        # Seed Initial Audit Log
        db.add(AuditLog(
            tenant_id=tenant.id,
            action="TENANT_WORKSPACE_INITIALIZED",
            entity_type="TENANT",
            entity_id=tenant.id,
            ip_address="127.0.0.1",
            change_details_json=json.dumps({"status": "SUCCESS", "market": "Hyderabad Commercial", "ts_rera_mode": "ACTIVE"})
        ))

        db.commit()
        print("[*] Database successfully initialized with verified institutional data.")
    else:
        print("[*] Database already populated for tenant:", tenant.name)
    db.close()

if __name__ == "__main__":
    seed_database()
