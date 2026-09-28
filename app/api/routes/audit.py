from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import AuditLog, User
from app.api.deps import get_current_user

router = APIRouter(prefix="/audit", tags=["Audit Trail"])

@router.get("")
def get_audit_logs(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).filter(
        AuditLog.tenant_id == current_user.tenant_id
    ).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return logs
