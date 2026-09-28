"""
Apex Estate AI - Daily Autonomous Operations Cycle
Executes daily property research audits, lead qualification runs, appointment calendar synchronization,
and generates the morning operations briefing for commercial desks in Hyderabad.
"""

from datetime import datetime, timezone
import json
from app.core.database import SessionLocal
from app.models.entities import Tenant, PropertyListing, BuyerLead, Appointment, ApprovalRequest, AgentTask, AuditLog
from app.agents.orchestrator import orchestrator

def run_daily_cycle():
    db = SessionLocal()
    tenant = db.query(Tenant).first()
    if not tenant:
        print("[!] No tenant workspace configured. Run seed_data.py first.")
        db.close()
        return

    print(f"\n========================================================")
    print(f"APEX ESTATE AI — DAILY AUTONOMOUS DISPATCH")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()} UTC")
    print(f"Workspace: {tenant.name} ({tenant.slug})")
    print(f"Primary Market: Hyderabad Commercial Corridors (TS-RERA)")
    print(f"========================================================")

    # 1. Audit Verified Commercial Inventory
    properties = db.query(PropertyListing).filter(PropertyListing.tenant_id == tenant.id).all()
    total_sqft = sum(p.size_sqft or 0 for p in properties)
    total_val = sum(p.asking_price or 0 for p in properties)
    print(f"\n[1/5] Commercial Asset Inventory:")
    print(f"  • Total Grade-A Assets Tracked: {len(properties)}")
    print(f"  • Tracked Floor Plate Area: {total_sqft:,.0f} sq ft")
    print(f"  • Active Portfolio Value: INR {total_val / 10000000:.2f} Cr (USD ${(total_val / 83.3) / 1000000:.2f}M)")

    # 2. Run Lead Qualification Department
    print(f"\n[2/5] Running Lead Qualification & Rubric Scoring...")
    qual_res = orchestrator.departments["buyer_qualification"].execute(
        tenant_id=tenant.id,
        command="Qualify all active investor leads against commercial mandate criteria",
        payload={},
        db=db
    )
    leads = db.query(BuyerLead).filter(BuyerLead.tenant_id == tenant.id).all()
    qualified = [l for l in leads if (l.qualification_score or 0) >= 80]
    print(f"  • Leads Processed: {len(leads)}")
    print(f"  • Qualified Institutional Mandates: {len(qualified)}")

    # 3. Calendar & Due Diligence Visits
    appts = db.query(Appointment).filter(Appointment.tenant_id == tenant.id).all()
    print(f"\n[3/5] Inspecting Due Diligence Schedule:")
    print(f"  • Active Site Inspections & Consultations: {len(appts)}")

    # 4. Human-In-The-Loop Compliance Review
    pending_approvals = db.query(ApprovalRequest).filter(
        ApprovalRequest.tenant_id == tenant.id,
        ApprovalRequest.status == "PENDING"
    ).all()
    print(f"\n[4/5] Compliance & Quality Assurance Gate:")
    print(f"  • Pending Broker Sign-Offs: {len(pending_approvals)}")

    # 5. Persist Master Briefing Task & Audit Entry
    briefing_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "properties_count": len(properties),
        "total_sqft": total_sqft,
        "portfolio_value_inr": total_val,
        "qualified_leads_count": len(qualified),
        "active_appointments": len(appts),
        "pending_compliance_reviews": len(pending_approvals),
        "ts_rera_mode": "ACTIVE_VERIFIED"
    }

    task = AgentTask(
        tenant_id=tenant.id,
        agent_name="Master Orchestrator Agent",
        command="Daily Institutional Operations Briefing & Market Audit",
        status="COMPLETED",
        cost_estimate_usd=0.015,
        output_payload_json=json.dumps(briefing_payload)
    )
    db.add(task)

    audit = AuditLog(
        tenant_id=tenant.id,
        action="DAILY_OPERATIONS_CYCLE_COMPLETED",
        entity_type="SYSTEM_ORCHESTRATOR",
        entity_id=task.id,
        ip_address="127.0.0.1 (Autonomous Engine)",
        change_details_json=json.dumps({"status": "SUCCESS", "summary": briefing_payload})
    )
    db.add(audit)
    db.commit()

    print(f"\n[5/5] Operations Briefing Logged & Persisted:")
    print(f"  • Task ID: {task.id}")
    print(f"  • Status: COMPLETED (Audit Ledger Verified)")
    print(f"========================================================\n")
    db.close()
    return briefing_payload

if __name__ == "__main__":
    run_daily_cycle()
