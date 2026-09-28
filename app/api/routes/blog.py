from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.agents.marketing_promotion import INSTITUTIONAL_BLOG_POSTS, MarketingPromotionAgent
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/blog", tags=["Institutional Market Insights & Blog"])

@router.get("")
def get_all_posts():
    return {
        "status": "SUCCESS",
        "count": len(INSTITUTIONAL_BLOG_POSTS),
        "posts": INSTITUTIONAL_BLOG_POSTS
    }

@router.get("/{slug}")
def get_post_by_slug(slug: str):
    for post in INSTITUTIONAL_BLOG_POSTS:
        if post["slug"] == slug or post["id"] == slug:
            return {"status": "SUCCESS", "post": post}
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/promote")
def trigger_promotion_campaign(payload: Dict[str, Any] = {}, db: Session = Depends(get_db)):
    agent = orchestrator.departments.get("marketing_promotion")
    if not agent:
        raise HTTPException(status_code=500, detail="Marketing agent unavailable")
    result = agent.execute(
        tenant_id="default",
        command=payload.get("command", "Launch institutional syndication & social distribution campaign"),
        payload=payload,
        db=db
    )
    return result
