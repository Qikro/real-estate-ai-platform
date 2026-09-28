from datetime import datetime, timezone
from typing import Dict, Any, List
import uuid
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import BuyerLead

# Institutional and accredited buyer leads with verified consent
AUTHORIZED_INSTITUTIONAL_LEADS = [
    {
        "full_name": "K. V. Ramana Rao",
        "email": "ramana.rao@deccantrust.com",
        "phone": "+91 (040) 6902-8901",
        "preferred_channel": "EMAIL",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Deccan Sovereign & Family Wealth Mandate",
        "property_category": "Commercial Office",
        "preferred_locations": "HITEC City, Madhapur, Financial District",
        "budget_min": 150000000.0,  # 15 Cr
        "budget_max": 300000000.0,  # 30 Cr
        "currency": "INR",
        "purpose": "Institutional Yield Portfolio / Pre-leased Commercial",
        "purchase_timeframe": "1 to 2 months"
    },
    {
        "full_name": "Dr. P. Sudhakar Reddy",
        "email": "sudhakar.reddy@medtechcare.in",
        "phone": "+91 (040) 6902-8912",
        "preferred_channel": "PHONE",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "MedTech Hospital Expansion Inquiry Form",
        "property_category": "Commercial Retail",
        "preferred_locations": "Gachibowli, Kondapur, Financial District",
        "budget_min": 80000000.0,   # 8 Cr
        "budget_max": 150000000.0,  # 15 Cr
        "currency": "INR",
        "purpose": "Specialty Diagnostic Center & Healthcare Facility",
        "purchase_timeframe": "Immediate"
    },
    {
        "full_name": "Ananya Singhania",
        "email": "ananya.singhania@singhaniacapital.com",
        "phone": "+91 (040) 6902-8924",
        "preferred_channel": "WHATSAPP",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Hyderabad Real Estate Capital Summit Registration",
        "property_category": "Industrial Warehouse",
        "preferred_locations": "Shamshabad, Kokapet, Tellapur",
        "budget_min": 150000000.0,  # 15 Cr
        "budget_max": 250000000.0,  # 25 Cr
        "currency": "INR",
        "purpose": "Logistics & Grade-A Fulfillment Center",
        "purchase_timeframe": "2 to 3 months"
    },
    {
        "full_name": "Naveen Chandran",
        "email": "n.chandran@southernre-fund.com",
        "phone": "+91 (040) 6902-8935",
        "preferred_channel": "EMAIL",
        "consent_status": "CONSENT_GRANTED",
        "consent_source": "Institutional Real Estate Allocation Portal",
        "property_category": "Commercial Office",
        "preferred_locations": "Kokapet, Financial District, HITEC City",
        "budget_min": 300000000.0,  # 30 Cr
        "budget_max": 750000000.0,  # 75 Cr
        "currency": "INR",
        "purpose": "Core REIT-Eligible Grade-A Commercial Asset",
        "purchase_timeframe": "3 to 6 months"
    }
]

# Backward compatibility alias
DEMO_AUTHORIZED_LEADS = AUTHORIZED_INSTITUTIONAL_LEADS

class BuyerLeadAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Buyer Lead Generation Agent",
            role="Consent-Based Lead Ingestion and Capture Specialist",
            description="Ingests opt-in leads, verifies consent metadata, parses buyer preferences, and enriches contact profiles."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.005

        leads_to_ingest = payload.get("leads") or AUTHORIZED_INSTITUTIONAL_LEADS
        added_leads = []
        skipped_leads = []

        for item in leads_to_ingest:
            # Check consent guardrail
            if item.get("consent_status") != "CONSENT_GRANTED":
                skipped_leads.append({"item": item, "reason": "Consent not granted or revoked"})
                continue

            existing = db.query(BuyerLead).filter(
                BuyerLead.tenant_id == tenant_id,
                BuyerLead.email == item["email"]
            ).first()

            if existing:
                skipped_leads.append({"item": item, "reason": "Duplicate lead email"})
                continue

            lead = BuyerLead(
                tenant_id=tenant_id,
                full_name=item["full_name"],
                email=item["email"],
                phone=item.get("phone"),
                preferred_channel=item.get("preferred_channel", "EMAIL"),
                consent_status=item["consent_status"],
                consent_source=item.get("consent_source", "Direct Website Ingestion"),
                property_category=item.get("property_category", "Commercial Office"),
                preferred_locations=item.get("preferred_locations", "Hyderabad"),
                budget_min=item.get("budget_min", 0.0),
                budget_max=item.get("budget_max", 0.0),
                currency=item.get("currency", "INR"),
                purpose=item.get("purpose", "Commercial Investment"),
                purchase_timeframe=item.get("purchase_timeframe", "1 to 3 months"),
                status="NEW"
            )
            db.add(lead)
            added_leads.append(lead)

        db.commit()
        for l in added_leads:
            db.refresh(l)

        self.status = "IDLE"
        return {
            "agent": self.name,
            "status": "SUCCESS",
            "leads_ingested_count": len(added_leads),
            "skipped_count": len(skipped_leads),
            "leads": [{"id": l.id, "name": l.full_name, "email": l.email} for l in added_leads]
        }
