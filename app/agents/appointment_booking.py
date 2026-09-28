from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.agents.base import BaseAgent
from app.models.entities import Appointment, BuyerLead

class AppointmentBookingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Appointment Booking Agent",
            role="Schedule Coordination and Calendar Management Specialist",
            description="Manages calendar availability, prevents double-booking, and coordinates property visit consultations."
        )

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1
        self.total_cost_usd += 0.006

        lead_id = payload.get("lead_id")
        title = payload.get("title", "Property Discovery Consultation")
        appointment_type = payload.get("appointment_type", "Property Visit")
        start_time_raw = payload.get("start_time")
        duration_minutes = payload.get("duration_minutes", 60)
        timezone_str = payload.get("timezone", "Asia/Kolkata")
        location_or_link = payload.get("location_or_link", "Financial District, Hyderabad / Google Meet")

        if not lead_id:
            lead = db.query(BuyerLead).filter(
                BuyerLead.tenant_id == tenant_id,
                BuyerLead.status == "QUALIFIED"
            ).first()
            if not lead:
                self.status = "IDLE"
                return {"status": "FAILED", "message": "No qualified leads available for scheduling."}
            lead_id = lead.id
        else:
            lead = db.query(BuyerLead).filter(BuyerLead.id == lead_id, BuyerLead.tenant_id == tenant_id).first()
            if not lead:
                self.status = "IDLE"
                return {"status": "FAILED", "message": "Lead not found."}

        # Parse or default start time
        if start_time_raw:
            if isinstance(start_time_raw, str):
                start_dt = datetime.fromisoformat(start_time_raw.replace("Z", "+00:00"))
            else:
                start_dt = start_time_raw
        else:
            # Tomorrow at 11:00 AM IST
            start_dt = datetime.now(timezone.utc) + timedelta(days=1)
            start_dt = start_dt.replace(hour=5, minute=30, second=0, microsecond=0)  # 11:00 AM IST is 05:30 UTC

        end_dt = start_dt + timedelta(minutes=duration_minutes)

        # Conflict Detection: check overlapping appointments
        conflict = db.query(Appointment).filter(
            Appointment.tenant_id == tenant_id,
            Appointment.status.in_(["SCHEDULED", "CONFIRMED"]),
            Appointment.start_time < end_dt,
            Appointment.end_time > start_dt
        ).first()

        if conflict:
            self.status = "IDLE"
            return {
                "status": "CONFLICT_DETECTED",
                "message": f"Time slot conflicts with existing appointment '{conflict.title}' ({conflict.start_time} - {conflict.end_time}).",
                "suggested_alternative": (start_dt + timedelta(hours=2)).isoformat()
            }

        appt = Appointment(
            tenant_id=tenant_id,
            lead_id=lead_id,
            title=f"{title} - {lead.full_name}",
            appointment_type=appointment_type,
            start_time=start_dt,
            end_time=end_dt,
            timezone=timezone_str,
            location_or_link=location_or_link,
            status="SCHEDULED",
            calendar_event_id=f"evt_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            notes=f"Scheduled for {lead.full_name} ({lead.preferred_locations} search).",
            reminder_sent=True
        )
        db.add(appt)
        db.commit()

        self.log_audit(
            db=db,
            tenant_id=tenant_id,
            action="APPOINTMENT_SCHEDULED",
            entity_type="Appointment",
            entity_id=appt.id,
            details={
                "title": appt.title,
                "start": appt.start_time.isoformat(),
                "end": appt.end_time.isoformat()
            }
        )

        self.status = "IDLE"
        return {
            "status": "SUCCESS",
            "message": f"Appointment successfully scheduled for {lead.full_name}.",
            "appointment_id": appt.id,
            "title": appt.title,
            "start_time": appt.start_time.isoformat(),
            "end_time": appt.end_time.isoformat(),
            "timezone": appt.timezone,
            "location": appt.location_or_link
        }
