import re
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.entities import PropertyListing

def normalize_text(text: Optional[str]) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def check_duplicate_property(
    db: Session,
    tenant_id: str,
    title: str,
    neighborhood: str,
    asking_price: float,
    size_sqft: float,
    original_url: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Returns (is_duplicate: bool, existing_id: Optional[str])
    """
    # 1. Direct URL match if URL is provided
    if original_url:
        existing = db.query(PropertyListing).filter(
            PropertyListing.tenant_id == tenant_id,
            PropertyListing.original_url == original_url
        ).first()
        if existing:
            return True, existing.id

    # 2. Heuristic attribute matching within neighborhood:
    # Same neighborhood, price within +/- 2%, size within +/- 2%
    candidates = db.query(PropertyListing).filter(
        PropertyListing.tenant_id == tenant_id,
        PropertyListing.neighborhood.ilike(f"%{neighborhood}%")
    ).all()

    norm_title = normalize_text(title)

    for item in candidates:
        price_diff = abs(item.asking_price - asking_price) / max(asking_price, 1)
        size_diff = abs(item.size_sqft - size_sqft) / max(size_sqft, 1)

        if price_diff <= 0.02 and size_diff <= 0.02:
            return True, item.id

        # Title similarity heuristic
        item_title = normalize_text(item.title)
        if norm_title and item_title and (norm_title in item_title or item_title in norm_title):
            if price_diff <= 0.05:
                return True, item.id

    return False, None
