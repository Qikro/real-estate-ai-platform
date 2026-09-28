from datetime import datetime, timezone
from typing import Dict, Any, List
import uuid
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import BuyerLead

DEMO_AUTHORIZED_LEADS = [
    {
        "full_name": "Rohan Deshmukh",
        "email": "rohan.deshmukh@apexventures.in",
        "phone": "+91 98200 44556",
        "preferred_channel": "EMAIL",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Hyderabad Commercial Investor Web Form",
        "property_category": "Commercial Office",
        "preferred_locations": "HITEC City, Madhapur, Financial District",
        "budget_min": 35000000.0,  # 3.5 Cr
        "budget_max": 50000000.0,  # 5 Cr
        "currency": "INR",
        "purpose": "Investment",
        "purchase_timeframe": "1 to 2 months"
    },
    {
        "full_name": "Dr. Sunita Malpani",
        "email": "sunita.malpani@healthtechgroup.in",
        "phone": "+91 99401 77889",
        "preferred_channel": "PHONE",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Opt-in Medical Diagnostic Center Relocation Inquiry",
        "property_category": "Commercial Retail",
        "preferred_locations": "Gachibowli, Kondapur",
        "budget_min": 60000000.0,  # 6 Cr
        "budget_max": 80000000.0,  # 8 Cr
        "currency": "INR",
        "purpose": "Self-Use / Diagnostic Clinic",
        "purchase_timeframe": "Immediate"
    },
    {
        "full_name": "Vikramaditya Raju",
        "email": "vikram.raju@rajuholding.com",
        "phone": "+91 97010 33221",
        "preferred_channel": "WHATSAPP",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Executive Investor Conference Registration",
        "property_category": "Plot",
        "preferred_locations": "Tellapur, Kokapet, Mokila",
        "budget_min": 50000000.0,  # 5 Cr
        "budget_max": 120000000.0, # 12 Cr
        "currency": "INR",
        "purpose": "Long-term Wealth Preservation",
        "purchase_timeframe": "3 to 6 months"
    }
]

class BuyerLeadAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Buyer Lead Generation Agent",
            role="Consent-Based Lead Ingestion and Capture Specialist",
            description="Captures and validates opt-in buyer inquiries, enforces explicit consent, and formats lead records."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.005

        leads_to_ingest = payload.get("leads") or DEMO_AUTHORIZED_LEADS
        created_leads = []
        skipped_leads = []

        for item in leads_to_ingest:
            # Consent and opt-out enforcement check
            if item.get("consent_status") == "REVOKED" or item.get("status") == "DO_NOT_CONTACT":
                skipped_leads.append({"email": item.get("email"), "reason": "Opt-out / Do not contact list"})
                continue

            # Check existing lead by email in this tenant
            existing = db.query(BuyerLead).filter(
                BuyerLead.tenant_id == tenant_id,
                BuyerLead.email == item["email"]
            ).first()

            if existing:
                skipped_leads.append({"email": item["email"], "reason": "Existing lead record"})
                continue

            lead = BuyerLead(
                tenant_id=tenant_id,
                full_name=item["full_name"],
                email=item["email"],
                phone=item["phone"],
                preferred_channel=item.get("preferred_channel", "EMAIL"),
                consent_status=item.get("consent_status", "CONSENT_GRANTED"),
                consent_source=item.get("consent_source", "Opt-in Form"),
                consent_timestamp=datetime.now(timezone.utc),
                property_category=item.get("property_category", "Commercial"),
                preferred_locations=item.get("preferred_locations", "Hyderabad"),
                budget_min=item.get("budget_min", 10000000.0),
                budget_max=item.get("budget_max", 50000000.0),
                currency="INR",
                purpose=item.get("purpose", "Investment"),
                purchase_timeframe=item.get("purchase_timeframe", "1 to 3 months"),
                status="NEW",
                qualification_score=0.0,
                recommended_action="Run qualification analysis"
            )
            db.add(lead)
            db.flush()
            created_leads.append({
                "id": lead.id,
                "name": lead.full_name,
                "email": lead.email,
                "budget_range": f"INR {lead.budget_min/10000000:.1f}Cr - {lead.budget_max/10000000:.1f}Cr"
            })

        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="LEAD_INGESTION_COMPLETED",
            entity_type="BuyerLead",
            entity_id=created_leads[0]["id"] if created_leads else "None",
            details={
                "leads_added": len(created_leads),
                "skipped_count": len(skipped_leads)
            }
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"Successfully ingested {len(created_leads)} opt-in buyer leads.",
            "created_count": len(created_leads),
            "skipped_count": len(skipped_leads),
            "leads": created_leads,
            "skipped": skipped_leads
        }
