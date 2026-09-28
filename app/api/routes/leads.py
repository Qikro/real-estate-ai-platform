from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io
from app.core.database import get_db
from app.models.entities import BuyerLead, User
from app.schemas.schemas import LeadCreate, LeadResponse
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/leads", tags=["Buyer Leads"])

@router.get("", response_model=List[LeadResponse])
def get_leads(
    status: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(BuyerLead).filter(BuyerLead.tenant_id == current_user.tenant_id)
    if status:
        query = query.filter(BuyerLead.status == status)
    if category:
        query = query.filter(BuyerLead.property_category.ilike(f"%{category}%"))
    return query.order_by(BuyerLead.created_at.desc()).all()

@router.post("", response_model=LeadResponse)
def create_lead(
    lead_in: LeadCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lead = BuyerLead(
        tenant_id=current_user.tenant_id,
        full_name=lead_in.full_name,
        email=lead_in.email,
        phone=lead_in.phone,
        preferred_channel=lead_in.preferred_channel,
        consent_status=lead_in.consent_status,
        consent_source=lead_in.consent_source,
        property_category=lead_in.property_category,
        preferred_locations=lead_in.preferred_locations,
        budget_min=lead_in.budget_min,
        budget_max=lead_in.budget_max,
        currency=lead_in.currency,
        purpose=lead_in.purpose,
        purchase_timeframe=lead_in.purchase_timeframe,
        status="NEW"
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Automatically score lead through qualification agent
    orchestrator.departments["buyer_qualification"].execute(
        tenant_id=current_user.tenant_id,
        command="Qualify single lead",
        payload={"lead_id": lead.id},
        db=db
    )
    db.refresh(lead)
    return lead

@router.post("/import-csv")
async def import_leads_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))

    imported = 0
    for row in reader:
        if not row.get("email") or not row.get("full_name"):
            continue
        lead = BuyerLead(
            tenant_id=current_user.tenant_id,
            full_name=row["full_name"],
            email=row["email"],
            phone=row.get("phone", "+91 90000 00000"),
            preferred_channel=row.get("preferred_channel", "EMAIL"),
            consent_status=row.get("consent_status", "CONSENT_GRANTED"),
            consent_source="CSV Import Batch",
            property_category=row.get("property_category", "Commercial"),
            preferred_locations=row.get("preferred_locations", "Hyderabad"),
            budget_min=float(row.get("budget_min", 10000000.0)),
            budget_max=float(row.get("budget_max", 50000000.0)),
            purpose=row.get("purpose", "Investment"),
            purchase_timeframe=row.get("purchase_timeframe", "1 to 3 months"),
            status="NEW"
        )
        db.add(lead)
        imported += 1

    db.commit()
    return {"status": "SUCCESS", "message": f"Successfully imported {imported} leads from CSV."}

@router.post("/qualify-all")
def qualify_all_leads(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.departments["buyer_qualification"].execute(
        tenant_id=current_user.tenant_id,
        command="Qualify all leads",
        payload={},
        db=db
    )
    return result
