from datetime import datetime, timezone, timedelta
import json
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.entities import (
    Tenant, User, PropertyListing, BuyerLead, Appointment,
    InvestorReport, ApprovalRequest, SalesProspect, FinancialTransaction, AuditLog, AgentTask
)
from app.agents.property_research import HYDERABAD_INVENTORY_FEED
from app.agents.buyer_lead import DEMO_AUTHORIZED_LEADS
from app.agents.sales_growth import TARGET_HYDERABAD_PROSPECTS
from app.services.pdf_generator import generate_pdf_report
from app.services.excel_generator import generate_excel_report

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if tenant exists
    tenant = db.query(Tenant).filter(Tenant.slug == "apex-realty-hyderabad").first()
    if not tenant:
        print("[*] Creating primary tenant workspace: Apex Realty Hyderabad")
        tenant = Tenant(
            name="Apex Realty & Capital Advisory",
            slug="apex-realty-hyderabad",
            tier="INVESTOR_OPS",
            status="ACTIVE",
            monthly_fee=1999.0,
            currency="USD",
            contact_email="admin@apexrealty.in"
        )
        db.add(tenant)
        db.flush()

        # Create Admin User
        admin_user = User(
            tenant_id=tenant.id,
            email="admin@estate.ai",
            hashed_password=get_password_hash("Admin@123456"),
            full_name="Quill Operations Lead",
            role="SUPER_ADMIN"
        )
        broker_user = User(
            tenant_id=tenant.id,
            email="broker@apexrealty.in",
            hashed_password=get_password_hash("Broker@123456"),
            full_name="Rajesh Varma",
            role="BROKER_ADMIN"
        )
        db.add(admin_user)
        db.add(broker_user)
        db.flush()

        # Seed Properties
        print("[*] Seeding verified Hyderabad commercial & residential inventory...")
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
                description=f"Verified Grade-A asset in {item['neighborhood']}. Prime investment potential.",
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
        for lead_item in DEMO_AUTHORIZED_LEADS:
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
                qualification_score=85.0,
                qualification_reason="Verified budget readiness, clear acquisition timeline, and written inquiry consent.",
                recommended_action="Schedule asset tour in HITEC City / Gachibowli"
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
            location_or_link="Mindspace Tech Zone, Madhapur, Hyderabad",
            status="SCHEDULED",
            notes="Client evaluating 3,500 sqft pre-leased office asset.",
            reminder_sent=True
        )
        db.add(appt)

        # Seed Sample Report with PDF & Excel
        print("[*] Generating baseline investor report...")
        report_data = {
            "title": f"Investment Memorandum: {created_props[0].title}",
            "client_name": created_leads[0].full_name,
            "preferred_locations": "HITEC City, Hyderabad",
            "target_budget": 50000000.0,
            "asking_price": created_props[0].asking_price,
            "gross_yield": 8.2,
            "cap_rate": 6.8,
            "monthly_expenses": 25000.0,
            "vacancy_rate_pct": 5.0,
            "maintenance_reserve_pct": 3.0,
            "executive_summary": "Institutional underwriting model for Grade-A Mindspace IT commercial asset.",
            "risks_and_caveats": "Tenant lease roll-over in 36 months; subject to local submarket absorption.",
            "legal_due_diligence_checklist": "- 30-year Encumbrance Certificate\n- HMDA Sanction Plan\n- RERA Certification"
        }
        pdf_f = f"report_{tenant.id[:8]}_demo.pdf"
        xlsx_f = f"model_{tenant.id[:8]}_demo.xlsx"
        pdf_path = generate_pdf_report(report_data, pdf_f)
        xlsx_path = generate_excel_report(report_data, xlsx_f)

        report = InvestorReport(
            tenant_id=tenant.id,
            title=report_data["title"],
            property_id=created_props[0].id,
            client_name=created_leads[0].full_name,
            target_budget=50000000.0,
            property_type=created_props[0].category,
            preferred_locations="HITEC City, Hyderabad",
            executive_summary=report_data["executive_summary"],
            asking_price=created_props[0].asking_price,
            estimated_rental_yield=8.2,
            gross_yield=8.2,
            cap_rate=6.8,
            monthly_expenses=25000.0,
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
                category=p["category"],
                city=p["city"],
                state=p["state"],
                website=p["website"],
                proposal_draft=f"Custom AI automation proposal for {p['business_name']}.",
                status="PROPOSAL_DRAFTED",
                estimated_value=p["estimated_value"]
            )
            db.add(prospect)
            db.flush()

            # Create approval request
            approval = ApprovalRequest(
                tenant_id=tenant.id,
                action_type="OUTBOUND_PROPOSAL_DISPATCH",
                description=f"Human authorization required to send proposal to {p['contact_person']} ({p['business_name']})",
                proposed_payload_json=json.dumps({"prospect_id": prospect.id, "email": p["email"]}),
                status="PENDING",
                requested_by_agent="Sales & Business Growth Agent"
            )
            db.add(approval)

        # Seed Financial Transactions (MRR tracking)
        print("[*] Seeding subscription transactions...")
        tx1 = FinancialTransaction(
            tenant_id=tenant.id,
            package_name="INVESTOR OPERATIONS",
            amount=1999.0,
            currency="USD",
            billing_interval="MONTHLY",
            status="PAID",
            payment_provider="Razorpay / Stripe Connect",
            ai_cost_usd=28.50,
            infrastructure_cost_usd=12.00,
            gross_margin_usd=1958.50
        )
        db.add(tx1)

        # Seed Initial Audit Log
        audit = AuditLog(
            tenant_id=tenant.id,
            user_id=admin_user.id,
            action="PLATFORM_INITIALIZATION_SUCCESS",
            entity_type="Platform",
            entity_id=tenant.id,
            change_details_json=json.dumps({"initialized": True, "target": "Hyderabad, Telangana"}),
            ip_address="127.0.0.1"
        )
        db.add(audit)

        db.commit()
        print("[+] Seeding completed successfully!")
    else:
        print("[*] Database already populated with tenant:", tenant.name)

    db.close()

if __name__ == "__main__":
    seed_database()
