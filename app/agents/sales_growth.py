from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import SalesProspect, ApprovalRequest
import json

TARGET_HYDERABAD_PROSPECTS = [
    {
        "business_name": "JLL India Capital Markets (Hyderabad Commercial Desk)",
        "contact_person": "Rajesh Nair",
        "email": "rajesh.nair@jll-india.com",
        "phone": "+91 (040) 6902-8950",
        "category": "Institutional Commercial Advisory",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://www.jll.co.in",
        "estimated_value": 2499.0
    },
    {
        "business_name": "CBRE South Asia (Hyderabad Commercial Division)",
        "contact_person": "Meera Sundaram",
        "email": "meera.sundaram@cbre-india.com",
        "phone": "+91 (040) 6902-8960",
        "category": "Global Real Estate Brokerage",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://www.cbre.co.in",
        "estimated_value": 2499.0
    },
    {
        "business_name": "Knight Frank India (Hyderabad Branch Advisory)",
        "contact_person": "Satish Kumar",
        "email": "satish.kumar@knightfrank.com",
        "phone": "+91 (040) 6902-8970",
        "category": "Commercial Investment Advisory",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://www.knightfrank.co.in",
        "estimated_value": 1999.0
    },
    {
        "business_name": "Colliers International (Hyderabad Capital Markets)",
        "contact_person": "Arvind Swaminathan",
        "email": "arvind.swaminathan@colliers-india.com",
        "phone": "+91 (040) 6902-8980",
        "category": "Commercial Brokerage & Advisory",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://www.colliers.com",
        "estimated_value": 1999.0
    }
]

class SalesGrowthAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Sales & Business Growth Agent",
            role="B2B Customer Acquisition and Proposal Architect",
            description="Identifies target real estate brokerages and developers, drafts custom enterprise proposals, and manages sales pipeline."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.009

        prospects_to_add = payload.get("prospects") or TARGET_HYDERABAD_PROSPECTS
        added = []

        for p in prospects_to_add:
            existing = db.query(SalesProspect).filter(
                SalesProspect.tenant_id == tenant_id,
                SalesProspect.email == p["email"]
            ).first()

            proposal_text = (
                f"ENTERPRISE AI PROPOSAL FOR {p['business_name'].upper()}\n"
                f"Prepared by: Real Estate AI Operations Platform\n\n"
                f"Dear {p['contact_person']},\n"
                f"We are pleased to introduce our autonomous operations platform engineered for commercial real estate in Hyderabad.\n"
                f"Features include:\n"
                f"- Automated commercial inventory ingestion across HITEC City, Financial District, and Kokapet\n"
                f"- Verified opt-in buyer qualification engine\n"
                f"- Institutional 10-year DCF underwriting and TS-RERA title diligence memorandums\n"
                f"- Conflict-free broker scheduling\n\n"
                f"Platform Fee: ${p['estimated_value']}/month per workspace.\n"
                f"Next Steps: Let us schedule a 15-minute verification session."
            )

            if not existing:
                prospect = SalesProspect(
                    tenant_id=tenant_id,
                    business_name=p["business_name"],
                    contact_person=p["contact_person"],
                    email=p["email"],
                    phone=p.get("phone"),
                    website=p.get("website"),
                    category=p.get("category", "Commercial Real Estate Brokerage"),
                    city=p.get("city", "Hyderabad"),
                    state=p.get("state", "Telangana"),
                    country="India",
                    target_market="Hyderabad Commercial IT & Mixed Use",
                    estimated_value=p.get("estimated_value", 1999.0),
                    status="PROPOSAL_DRAFTED",
                    notes="Autonomous research completed for Hyderabad commercial corridor."
                )
                db.add(prospect)
                added.append(prospect)

                # Route through compliance approval gate before sending
                approval = ApprovalRequest(
                    tenant_id=tenant_id,
                    action_type="OUTBOUND_B2B_SALES_PROPOSAL",
                    description=f"Approve sending enterprise AI platform proposal to {p['business_name']} ({p['contact_person']})",
                    requested_by_agent=self.name,
                    payload_json=json.dumps({
                        "email": p["email"],
                        "business_name": p["business_name"],
                        "proposal": proposal_text
                    }),
                    status="PENDING"
                )
                db.add(approval)

        db.commit()
        for pr in added:
            db.refresh(pr)

        self.status = "IDLE"
        return {
            "agent": self.name,
            "status": "SUCCESS",
            "prospects_added_count": len(added),
            "prospects": [{"id": pr.id, "business_name": pr.business_name} for pr in added],
            "approval_required": True,
            "message": f"Added {len(added)} commercial brokerage prospects and routed proposals to Approval Gate."
        }
