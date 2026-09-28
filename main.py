import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import (
    auth, agents, properties, leads, appointments,
    reports, approvals, crm, sales, finance, audit
)
from seed_data import seed_database

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Institutional AI Operations Platform for Real Estate Brokerages, Investors & Developers in Hyderabad, India."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(properties.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(crm.router, prefix="/api")
app.include_router(sales.router, prefix="/api")
app.include_router(finance.router, prefix="/api")
app.include_router(audit.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    try:
        seed_database()
    except Exception as e:
        print(f"[*] Startup seed notice: {e}")

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "target_city": settings.INITIAL_TARGET_CITY,
        "database": "CONNECTED",
        "ai_orchestrator": "ONLINE"
    }

@app.get("/api/cron/daily-ops")
@app.post("/api/cron/daily-ops")
def run_cron_daily_ops():
    from daily_cycle import run_daily_cycle
    summary = run_daily_cycle()
    return {
        "status": "SUCCESS",
        "message": "Daily institutional cycle completed",
        "summary": summary
    }

# Mount static frontend
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
