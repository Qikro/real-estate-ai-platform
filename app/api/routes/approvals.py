from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import ApprovalRequest, User
from app.schemas.schemas import ApprovalResponse, ApprovalDecisionRequest
from app.api.deps import get_current_user

router = APIRouter(prefix="/approvals", tags=["Compliance Approvals"])

@router.get("", response_model=List[ApprovalResponse])
def get_approvals(
    status: str = "PENDING",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ApprovalRequest).filter(ApprovalRequest.tenant_id == current_user.tenant_id)
    if status != "ALL":
        query = query.filter(ApprovalRequest.status == status)
    return query.order_by(ApprovalRequest.created_at.desc()).all()

@router.post("/{approval_id}/decision", response_model=ApprovalResponse)
def decide_approval(
    approval_id: str,
    req: ApprovalDecisionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    approval = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == approval_id,
        ApprovalRequest.tenant_id == current_user.tenant_id
    ).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    if req.decision not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Decision must be APPROVED or REJECTED")

    approval.status = req.decision
    approval.comment = req.comment
    approval.reviewed_by_user_id = current_user.id
    approval.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(approval)
    return approval
