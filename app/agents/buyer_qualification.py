from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import BuyerLead, PropertyListing

class BuyerQualificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Buyer Qualification Agent",
            role="Lead Qualification and Matching Specialist",
            description="Evaluates buyer financial parameters, timeline, and location preferences against verified inventory using non-discriminatory criteria."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.007

        lead_id = payload.get("lead_id")
        leads_query = db.query(BuyerLead).filter(BuyerLead.tenant_id == tenant_id)
        if lead_id:
            leads_query = leads_query.filter(BuyerLead.id == lead_id)
        else:
            # Qualify all new or pending leads
            leads_query = leads_query.filter(BuyerLead.status.in_(["NEW", "INFORMATION_PENDING", "CONTACTED"]))

        leads = leads_query.all()
        qualified_records = []

        # Fetch available inventory for matching
        properties = db.query(PropertyListing).filter(
            PropertyListing.tenant_id == tenant_id,
            PropertyListing.availability_status == "AVAILABLE"
        ).all()

        for lead in leads:
            score = 0.0
            reasons = []
            missing = []

            # 1. Budget viability (35 points)
            if lead.budget_max and lead.budget_max > 0:
                score += 35.0
                reasons.append(f"Budget specified ({lead.currency} {lead.budget_min/10000000:.1f}Cr - {lead.budget_max/10000000:.1f}Cr)")
            else:
                missing.append("Specific investment budget range")

            # 2. Timeline clarity (25 points)
            if lead.purchase_timeframe and lead.purchase_timeframe != "Unspecified":
                score += 25.0
                reasons.append(f"Clear acquisition timeframe: {lead.purchase_timeframe}")
            else:
                missing.append("Expected purchase/closing timeframe")

            # 3. Specific asset category & location (25 points)
            if lead.property_category and lead.preferred_locations:
                score += 25.0
                reasons.append(f"Targeting {lead.property_category} in {lead.preferred_locations}")
            else:
                missing.append("Precise location and asset type requirements")

            # 4. Verified Consent & Contactibility (15 points)
            if lead.consent_status == "CONSENT_GRANTED":
                score += 15.0
                reasons.append("Verified opt-in consent on record")
            else:
                missing.append("Explicit contact permission confirmation")

            lead.qualification_score = score

            # Matching properties
            matching_props = []
            for prop in properties:
                if prop.asking_price <= lead.budget_max * 1.15:  # within 15% flexibility
                    # Check neighborhood overlap
                    if any(loc.strip().lower() in prop.neighborhood.lower() for loc in lead.preferred_locations.split(",")):
                        matching_props.append(prop.title)

            if score >= 75.0:
                lead.status = "QUALIFIED"
                lead.recommended_action = f"Schedule property consultation ({len(matching_props)} matching assets identified)"
            elif score >= 50.0:
                lead.status = "FOLLOW_UP"
                lead.recommended_action = "Request missing budget or location details"
            else:
                lead.status = "INFORMATION_PENDING"
                lead.recommended_action = "Send qualification inquiry questionnaire"

            lead.qualification_reason = "; ".join(reasons)
            lead.missing_information = "; ".join(missing) if missing else "None. Profile complete."
            lead.last_interaction_date = datetime.now(timezone.utc)

            qualified_records.append({
                "lead_id": lead.id,
                "name": lead.full_name,
                "score": score,
                "status": lead.status,
                "matching_properties_count": len(matching_props),
                "action": lead.recommended_action
            })

        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="LEAD_QUALIFICATION_COMPLETED",
            entity_type="BuyerLead",
            entity_id=leads[0].id if leads else "None",
            details={"qualified_count": len(qualified_records)}
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"Evaluated and updated qualification scores for {len(qualified_records)} leads.",
            "results": qualified_records
        }
