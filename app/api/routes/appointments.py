from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import Appointment, User
from app.schemas.schemas import AppointmentCreate, AppointmentResponse
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("", response_model=List[AppointmentResponse])
def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appts = db.query(Appointment).filter(
        Appointment.tenant_id == current_user.tenant_id
    ).order_by(Appointment.start_time.asc()).all()
    return appts

@router.post("/schedule")
def schedule_appointment(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["appointment_booking"].execute(
        tenant_id=current_user.tenant_id,
        command="Schedule appointment",
        payload=payload,
        db=db
    )
    return result
