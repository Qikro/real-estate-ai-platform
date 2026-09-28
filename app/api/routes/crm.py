from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import Tenant, User
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/crm", tags=["CRM & Client Management"])

@router.get("/summary")
def get_crm_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["crm_manager"].execute(
        tenant_id=current_user.tenant_id,
        command="Get CRM Summary",
        payload={},
        db=db
    )
    return result

@router.get("/tenants")
def list_tenants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only super admin or current tenant info
    if current_user.role == "SUPER_ADMIN":
        tenants = db.query(Tenant).all()
    else:
        tenants = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).all()
    return tenants
