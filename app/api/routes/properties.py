from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.entities import PropertyListing, User
from app.schemas.schemas import PropertyCreate, PropertyResponse
from app.api.deps import get_current_user
from app.services.dedup_service import check_duplicate_property

router = APIRouter(prefix="/properties", tags=["Property Research"])

@router.get("", response_model=List[PropertyResponse])
def get_properties(
    category: Optional[str] = None,
    neighborhood: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(PropertyListing).filter(PropertyListing.tenant_id == current_user.tenant_id)
    if category:
        query = query.filter(PropertyListing.category.ilike(f"%{category}%"))
    if neighborhood:
        query = query.filter(PropertyListing.neighborhood.ilike(f"%{neighborhood}%"))
    if min_price:
        query = query.filter(PropertyListing.asking_price >= min_price)
    if max_price:
        query = query.filter(PropertyListing.asking_price <= max_price)

    return query.order_by(PropertyListing.created_at.desc()).all()

@router.post("", response_model=PropertyResponse)
def create_property(
    prop_in: PropertyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Deduplication check
    is_dup, existing_id = check_duplicate_property(
        db=db,
        tenant_id=current_user.tenant_id,
        title=prop_in.title,
        neighborhood=prop_in.neighborhood,
        asking_price=prop_in.asking_price,
        size_sqft=prop_in.size_sqft,
        original_url=prop_in.original_url
    )

    price_per_sqft = round(prop_in.asking_price / prop_in.size_sqft, 2) if prop_in.size_sqft > 0 else 0.0

    prop = PropertyListing(
        tenant_id=current_user.tenant_id,
        title=prop_in.title,
        category=prop_in.category,
        city=prop_in.city,
        neighborhood=prop_in.neighborhood,
        address=prop_in.address,
        asking_price=prop_in.asking_price,
        currency=prop_in.currency,
        size_sqft=prop_in.size_sqft,
        unit=prop_in.unit,
        price_per_sqft=price_per_sqft,
        description=prop_in.description,
        listing_source=prop_in.listing_source,
        original_url=prop_in.original_url,
        availability_status=prop_in.availability_status,
        contact_name=prop_in.contact_name,
        contact_phone=prop_in.contact_phone,
        contact_email=prop_in.contact_email,
        legal_verification_status=prop_in.legal_verification_status,
        confidence_label="VERIFIED_FROM_SOURCE" if prop_in.original_url else "PARTIALLY_VERIFIED",
        is_duplicate=is_dup,
        duplicate_of_id=existing_id,
        investment_notes=prop_in.investment_notes
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property_by_id(
    property_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prop = db.query(PropertyListing).filter(
        PropertyListing.id == property_id,
        PropertyListing.tenant_id == current_user.tenant_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property listing not found")
    return prop
