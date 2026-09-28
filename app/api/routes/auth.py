from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.entities import User, Tenant
from app.schemas.schemas import TokenResponse, LoginRequest, RegisterTenantRequest
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    access_token = create_access_token(data={"sub": user.id, "tenant_id": user.tenant_id, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "tenant_id": tenant.id if tenant else "",
        "tenant_name": tenant.name if tenant else "Default Workspace"
    }

@router.post("/login", response_model=TokenResponse)
def login_json(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    access_token = create_access_token(data={"sub": user.id, "tenant_id": user.tenant_id, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "tenant_id": tenant.id if tenant else "",
        "tenant_name": tenant.name if tenant else "Default Workspace"
    }

@router.post("/register-tenant", response_model=TokenResponse)
def register_tenant(req: RegisterTenantRequest, db: Session = Depends(get_db)):
    existing_tenant = db.query(Tenant).filter(Tenant.slug == req.tenant_slug).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant slug already in use")

    existing_user = db.query(User).filter(User.email == req.admin_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    fee_map = {"STARTER": 299.0, "GROWTH": 999.0, "INVESTOR_OPS": 1999.0}
    tenant = Tenant(
        name=req.tenant_name,
        slug=req.tenant_slug,
        tier=req.tier,
        monthly_fee=fee_map.get(req.tier, 999.0),
        currency="USD",
        contact_email=req.admin_email
    )
    db.add(tenant)
    db.flush()

    user = User(
        tenant_id=tenant.id,
        email=req.admin_email,
        hashed_password=get_password_hash(req.admin_password),
        full_name=req.admin_name,
        role="BROKER_ADMIN"
    )
    db.add(user)
    db.commit()

    access_token = create_access_token(data={"sub": user.id, "tenant_id": tenant.id, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "tenant_id": tenant.id,
        "tenant_name": tenant.name
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id,
        "tenant_name": tenant.name if tenant else "",
        "tenant_tier": tenant.tier if tenant else ""
    }
