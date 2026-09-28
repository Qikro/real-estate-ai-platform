from fastapi.testclient import TestClient
from main import app
from app.core.database import SessionLocal, Base, engine
from seed_data import seed_database

def test_api_and_static_frontend():
    seed_database()
    client = TestClient(app)

    # Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "HEALTHY"

    # Static UI
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "Real Estate AI Operations Platform" in res_ui.text

    # Login
    res_login = client.post("/api/auth/login", json={"email": "admin@estate.ai", "password": "Admin@123456"})
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Properties
    res_props = client.get("/api/properties", headers=headers)
    assert res_props.status_code == 200
    assert len(res_props.json()) >= 1

    # Leads
    res_leads = client.get("/api/leads", headers=headers)
    assert res_leads.status_code == 200
    assert len(res_leads.json()) >= 1

    # Appointments
    res_appts = client.get("/api/appointments", headers=headers)
    assert res_appts.status_code == 200
    assert len(res_appts.json()) >= 1

    # Reports
    res_reports = client.get("/api/reports", headers=headers)
    assert res_reports.status_code == 200
    assert len(res_reports.json()) >= 1

    # Agents
    res_agents = client.get("/api/agents", headers=headers)
    assert res_agents.status_code == 200
    assert len(res_agents.json()["agents"]) == 10

    # Finance
    res_fin = client.get("/api/finance/metrics", headers=headers)
    assert res_fin.status_code == 200
    assert res_fin.json()["status"] == "SUCCESS"
