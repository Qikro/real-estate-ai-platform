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
    assert res_health.json().get("paypal_gateway") == "ONLINE"
    assert res_health.json().get("campaign_interval") == "10_MINUTES_ACTIVE"

    # Static UI
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "Linkmerce Online" in res_ui.text

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

    # Agents (11 specialized departments)
    res_agents = client.get("/api/agents", headers=headers)
    assert res_agents.status_code == 200
    assert len(res_agents.json()["agents"]) >= 11

    # Finance Metrics
    res_fin = client.get("/api/finance/metrics", headers=headers)
    assert res_fin.status_code == 200
    assert res_fin.json()["status"] == "SUCCESS"
    assert "paypal_integration" in res_fin.json()["metrics"]

    # Blog API
    res_blog = client.get("/api/blog")
    assert res_blog.status_code == 200
    assert len(res_blog.json()["posts"]) >= 3

    # PayPal Config
    res_paypal_cfg = client.get("/api/paypal/config")
    assert res_paypal_cfg.status_code == 200
    assert res_paypal_cfg.json()["status"] == "CONFIGURED"

    # PayPal Create Order
    res_paypal_create = client.post("/api/paypal/create-order", json={
        "amount": 1000.0,
        "currency": "USD",
        "package_name": "COMMISSION_ESCROW",
        "description": "Mindspace 12D Pre-Lease Commission Payout"
    })
    assert res_paypal_create.status_code == 200
    order_id = res_paypal_create.json()["order_id"]
    assert "PAYPAL-ORD-" in order_id

    # PayPal Capture Order
    res_paypal_capture = client.post("/api/paypal/capture-order", json={
        "order_id": order_id,
        "amount": 1000.0,
        "currency": "USD",
        "package_name": "COMMISSION_ESCROW",
        "payer_email": "investor@linkmerce.online",
        "payer_name": "Institutional Investor Desk"
    })
    assert res_paypal_capture.status_code == 200
    assert res_paypal_capture.json()["status"] == "COMPLETED"
    assert res_paypal_capture.json()["amount"] == 1000.0
    assert res_paypal_capture.json()["net_payout_usd"] > 950.0

    # PayPal Transactions
    res_paypal_txs = client.get("/api/paypal/transactions")
    assert res_paypal_txs.status_code == 200
    assert res_paypal_txs.json()["count"] >= 1
    assert res_paypal_txs.json()["total_volume_usd"] >= 1000.0

    # Daily Commission Target Telemetry
    res_comm_target = client.get("/api/finance/commission-target")
    assert res_comm_target.status_code == 200
    assert res_comm_target.json()["daily_target_usd"] == 1000.0
    assert res_comm_target.json()["progress_percent"] == 100.0

    # 10-Minute Campaign & Teammate Sync Endpoint
    res_campaign = client.post("/api/cron/campaign-ops")
    assert res_campaign.status_code == 200
    assert res_campaign.json()["status"] == "SUCCESS"
    assert "teammates" in res_campaign.json()["summary"]
    assert "val" in res_campaign.json()["summary"]["teammates"]
    assert "scout" in res_campaign.json()["summary"]["teammates"]
    assert "lex" in res_campaign.json()["summary"]["teammates"]
    assert "echo" in res_campaign.json()["summary"]["teammates"]
    assert "aria" in res_campaign.json()["summary"]["teammates"]
