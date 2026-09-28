import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.entities import InvestorReport, User
from app.schemas.schemas import InvestorReportResponse
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/reports", tags=["Investor Reports"])

@router.get("", response_model=List[InvestorReportResponse])
def get_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(InvestorReport).filter(
        InvestorReport.tenant_id == current_user.tenant_id
    ).order_by(InvestorReport.created_at.desc()).all()
    return reports

@router.post("/generate")
def generate_report(
    payload: dict = {},
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["investor_reporting"].execute(
        tenant_id=current_user.tenant_id,
        command="Generate investor memorandum and financial underwriting model",
        payload=payload,
        db=db
    )
    return result

@router.get("/{report_id}/download/pdf")
def download_pdf(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(InvestorReport).filter(
        InvestorReport.id == report_id,
        InvestorReport.tenant_id == current_user.tenant_id
    ).first()
    if not report or not report.pdf_path or not os.path.exists(report.pdf_path):
        raise HTTPException(status_code=404, detail="PDF report not found")
    return FileResponse(
        report.pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(report.pdf_path)
    )

@router.get("/{report_id}/download/xlsx")
def download_xlsx(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(InvestorReport).filter(
        InvestorReport.id == report_id,
        InvestorReport.tenant_id == current_user.tenant_id
    ).first()
    if not report or not report.xlsx_path or not os.path.exists(report.xlsx_path):
        raise HTTPException(status_code=404, detail="Excel financial model not found")
    return FileResponse(
        report.xlsx_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(report.xlsx_path)
    )
