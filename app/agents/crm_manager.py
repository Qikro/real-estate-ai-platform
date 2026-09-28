from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import Tenant, PropertyListing, BuyerLead, Appointment, InvestorReport

class CRMManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CRM & Client Management Agent",
            role="Tenant Isolation, Pipeline Tracking and Workspace Administrator",
            description="Coordinates multi-tenant client records, calculates pipeline summaries, enforces permissions, and maintains audit trails."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.004

        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            self.status = "IDLE"
            return {"status": "FAILED", "message": "Tenant not found."}

        # Gather metrics isolated strictly to this tenant
        prop_count = db.query(PropertyListing).filter(PropertyListing.tenant_id == tenant_id).count()
        lead_count = db.query(BuyerLead).filter(BuyerLead.tenant_id == tenant_id).count()
        qualified_count = db.query(BuyerLead).filter(
            BuyerLead.tenant_id == tenant_id,
            BuyerLead.status == "QUALIFIED"
        ).count()
        appt_count = db.query(Appointment).filter(Appointment.tenant_id == tenant_id).count()
        report_count = db.query(InvestorReport).filter(InvestorReport.tenant_id == tenant_id).count()

        summary = {
            "tenant_name": tenant.name,
            "subscription_tier": tenant.tier,
            "monthly_fee": tenant.monthly_fee,
            "currency": tenant.currency,
            "active_properties": prop_count,
            "total_leads": lead_count,
            "qualified_leads": qualified_count,
            "scheduled_appointments": appt_count,
            "generated_reports": report_count,
            "pipeline_conversion_rate": f"{round((qualified_count / max(lead_count, 1)) * 100, 1)}%"
        }

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"CRM metrics computed for workspace: {tenant.name}",
            "summary": summary
        }
