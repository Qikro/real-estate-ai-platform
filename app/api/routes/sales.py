from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import SalesProspect, User
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/sales", tags=["Sales & Growth"])

@router.get("/prospects")
def list_prospects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prospects = db.query(SalesProspect).filter(
        SalesProspect.tenant_id == current_user.tenant_id
    ).order_by(SalesProspect.created_at.desc()).all()
    return prospects

@router.post("/discover")
def trigger_sales_discovery(
    payload: dict = {},
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["sales_growth"].execute(
        tenant_id=current_user.tenant_id,
        command="Discover B2B real estate agency prospects",
        payload=payload,
        db=db
    )
    return result
