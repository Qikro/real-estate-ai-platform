from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
import json
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import PropertyListing, BuyerLead, ApprovalRequest

class ComplianceQAAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Quality & Compliance Agent",
            role="Regulatory Verification, Data Integrity and Approval Gatekeeper",
            description="Audits data freshness, validates source attribution, flags stale listings, and enforces human-in-the-loop approval gates."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.005

        action = payload.get("action", "AUDIT_WORKSPACE")

        if action == "REQUEST_APPROVAL":
            # Create a pending approval gate
            action_type = payload.get("action_type", "OUTBOUND_COMMUNICATION")
            description = payload.get("description", "Agent requests authorization to send lead qualification outreach.")
            proposed_payload = payload.get("proposed_payload", {})

            approval = ApprovalRequest(
                tenant_id=tenant_id,
                action_type=action_type,
                description=description,
                proposed_payload_json=json.dumps(proposed_payload),
                status="PENDING",
                requested_by_agent=payload.get("requested_by", "Operations Agent")
            )
            db.add(approval)
            db.commit()

            self.status = "IDLE"
            return {
                "status": "APPROVAL_REQUIRED",
                "message": f"Action [{action_type}] held at Compliance Gate. Awaiting human broker authorization.",
                "approval_id": approval.id,
                "description": description
            }

        # Otherwise audit data freshness & completeness
        properties = db.query(PropertyListing).filter(PropertyListing.tenant_id == tenant_id).all()
        flagged_properties = []

        now = datetime.now(timezone.utc)
        for p in properties:
            # Check if source URL exists
            if not p.original_url:
                p.confidence_label = "PARTIALLY_VERIFIED"
                flagged_properties.append({"id": p.id, "title": p.title, "issue": "Missing verified original source URL"})

            # Check if verified date is older than 60 days
            # If naive datetime, make comparable
            p_date = p.last_verified_date
            if p_date.tzinfo is None:
                p_date = p_date.replace(tzinfo=timezone.utc)

            if (now - p_date) > timedelta(days=60):
                p.confidence_label = "OUTDATED"
                flagged_properties.append({"id": p.id, "title": p.title, "issue": "Listing verification older than 60 days"})

        leads = db.query(BuyerLead).filter(BuyerLead.tenant_id == tenant_id).all()
        flagged_leads = []
        for lead in leads:
            if lead.consent_status != "CONSENT_GRANTED":
                flagged_leads.append({"id": lead.id, "name": lead.full_name, "issue": "Consent not explicitly verified"})

        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="COMPLIANCE_AUDIT_COMPLETED",
            entity_type="ComplianceAudit",
            entity_id="audit_summary",
            details={
                "properties_flagged": len(flagged_properties),
                "leads_flagged": len(flagged_leads)
            }
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": "Quality assurance audit complete.",
            "total_properties_audited": len(properties),
            "flagged_properties_count": len(flagged_properties),
            "flagged_leads_count": len(flagged_leads),
            "flagged_properties": flagged_properties,
            "flagged_leads": flagged_leads
        }
