from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import FinancialTransaction, User
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/finance", tags=["Finance & Revenue"])

@router.get("/metrics")
def get_revenue_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["finance_monitor"].execute(
        tenant_id=current_user.tenant_id,
        command="Get Revenue Metrics",
        payload={},
        db=db
    )
    return result

@router.get("/transactions")
def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    txs = db.query(FinancialTransaction).filter(
        FinancialTransaction.tenant_id == current_user.tenant_id
    ).order_by(FinancialTransaction.transaction_date.desc()).all()
    return txs
