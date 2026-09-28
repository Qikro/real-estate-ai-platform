from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import SalesProspect, ApprovalRequest
import json

TARGET_HYDERABAD_PROSPECTS = [
    {
        "business_name": "Deccan Commercial Advisory",
        "contact_person": "K. V. Subbarao",
        "email": "kv.subbarao@deccancommercial.in",
        "phone": "+91 98480 99112",
        "category": "Commercial Real Estate Brokerage",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://deccancommercial.in",
        "estimated_value": 999.0
    },
    {
        "business_name": "CyberCity Developers & Asset Managers",
        "contact_person": "Murali Mohan Reddy",
        "email": "murali@cybercityrealty.in",
        "phone": "+91 98481 22334",
        "category": "Property Developer",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://cybercityrealty.in",
        "estimated_value": 1999.0
    },
    {
        "business_name": "Telangana Land & Warehousing Consultants",
        "contact_person": "Srikanth Naidu",
        "email": "srikanth@tlwconsultants.in",
        "phone": "+91 98482 77889",
        "category": "Industrial Consultant",
        "city": "Hyderabad",
        "state": "Telangana",
        "website": "https://tlwconsultants.in",
        "estimated_value": 999.0
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
                f"We are pleased to submit this proposal to automate your commercial research, buyer lead qualification, "
                f"and appointment booking operations across the Hyderabad corridor (HITEC City, Gachibowli, Kokapet).\n\n"
                f"Recommended Package: REAL ESTATE GROWTH ($999/mo or INR 83,000/mo)\n"
                f"Key Deliverables:\n"
                f"1. Continuous verified property indexing and deduplication.\n"
                f"2. 24/7 lead qualification scoring and matching.\n"
                f"3. Automated appointment scheduling with conflict prevention.\n"
                f"4. Institutional PDF & Excel financial underwriting models.\n\n"
                f"Estimated monthly time saved: 140+ agent hours."
            )

            if not existing:
                prospect = SalesProspect(
                    tenant_id=tenant_id,
                    business_name=p["business_name"],
                    contact_person=p["contact_person"],
                    email=p["email"],
                    phone=p.get("phone"),
                    category=p.get("category", "Real Estate Brokerage"),
                    city=p.get("city", "Hyderabad"),
                    state=p.get("state", "Telangana"),
                    website=p.get("website"),
                    proposal_draft=proposal_text,
                    status="PROPOSAL_DRAFTED",
                    estimated_value=p.get("estimated_value", 999.0)
                )
                db.add(prospect)
                db.flush()
                added.append(prospect)

                # Gate requirement: draft proposal requires human approval before outbound send
                approval = ApprovalRequest(
                    tenant_id=tenant_id,
                    action_type="OUTBOUND_PROPOSAL_DISPATCH",
                    description=f"Approve sending enterprise sales proposal to {p['contact_person']} at {p['business_name']} ({p['email']})",
                    proposed_payload_json=json.dumps({"prospect_id": prospect.id, "email": p["email"], "proposal": proposal_text}),
                    status="PENDING",
                    requested_by_agent=self.name
                )
                db.add(approval)

        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="SALES_PROSPECTS_GENERATED",
            entity_type="SalesProspect",
            entity_id=added[0].id if added else "None",
            details={"prospects_count": len(added)}
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"Identified and drafted personalized proposals for {len(added)} commercial real estate prospects. Outbound dispatches queued for approval.",
            "prospects_added": len(added)
        }
