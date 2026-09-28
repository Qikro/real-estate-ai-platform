from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import json
import re
from sqlalchemy.orm import Session

from app.agents.base import BaseAgent
from app.agents.property_research import PropertyResearchAgent
from app.agents.buyer_lead import BuyerLeadAgent
from app.agents.buyer_qualification import BuyerQualificationAgent
from app.agents.appointment_booking import AppointmentBookingAgent
from app.agents.investor_reporting import InvestorReportingAgent
from app.agents.crm_manager import CRMManagerAgent
from app.agents.compliance_qa import ComplianceQAAgent
from app.agents.sales_growth import SalesGrowthAgent
from app.agents.finance_monitor import FinanceMonitorAgent
from app.models.entities import AgentTask, ApprovalRequest

class MasterOperationsOrchestrator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Master AI Operations Manager",
            role="Central Operations Orchestrator and Workflow Director",
            description="Coordinates all 9 specialized departments, parses business commands, queues tasks, handles retries, and compiles daily performance reports."
        )
        # Register specialized department agents
        self.departments: Dict[str, BaseAgent] = {
            "property_research": PropertyResearchAgent(),
            "buyer_lead": BuyerLeadAgent(),
            "buyer_qualification": BuyerQualificationAgent(),
            "appointment_booking": AppointmentBookingAgent(),
            "investor_reporting": InvestorReportingAgent(),
            "crm_manager": CRMManagerAgent(),
            "compliance_qa": ComplianceQAAgent(),
            "sales_growth": SalesGrowthAgent(),
            "finance_monitor": FinanceMonitorAgent()
        }

    def get_agent_registry(self) -> List[Dict[str, Any]]:
        agents_info = [self.to_dict()]
        for dept in self.departments.values():
            agents_info.append(dept.to_dict())
        return agents_info

    def parse_intent(self, command: str) -> Dict[str, Any]:
        """
        Interprets natural language commands into target departments and execution payloads.
        """
        cmd_lower = command.lower()

        if any(w in cmd_lower for w in ["find", "research", "property", "commercial", "industrial", "warehouse", "office", "residential", "listing"]):
            if "industrial" in cmd_lower or "warehouse" in cmd_lower:
                return {"target": "property_research", "payload": {"category": "Industrial"}}
            elif "commercial" in cmd_lower:
                return {"target": "property_research", "payload": {"category": "Commercial"}}
            elif "residential" in cmd_lower:
                return {"target": "property_research", "payload": {"category": "Residential"}}
            return {"target": "property_research", "payload": {}}

        elif any(w in cmd_lower for w in ["buyer", "leads", "lead gen", "potential buyers", "inquiries"]):
            return {"target": "buyer_lead", "payload": {}}

        elif any(w in cmd_lower for w in ["qualify", "qualification", "score leads", "qualified"]):
            return {"target": "buyer_qualification", "payload": {}}

        elif any(w in cmd_lower for w in ["schedule", "appointment", "calendar", "visit", "consultation", "booking"]):
            return {"target": "appointment_booking", "payload": {}}

        elif any(w in cmd_lower for w in ["investor", "report", "underwriting", "memorandum", "yield", "pdf"]):
            return {"target": "investor_reporting", "payload": {}}

        elif any(w in cmd_lower for w in ["sales", "prospect", "pipeline", "b2b", "outreach"]):
            return {"target": "sales_growth", "payload": {}}

        elif any(w in cmd_lower for w in ["compliance", "audit", "verify", "gate", "stale"]):
            return {"target": "compliance_qa", "payload": {}}

        elif any(w in cmd_lower for w in ["revenue", "finance", "mrr", "cost", "financial", "margin"]):
            return {"target": "finance_monitor", "payload": {}}

        elif any(w in cmd_lower for w in ["crm", "client", "workspace", "status"]):
            return {"target": "crm_manager", "payload": {}}

        # Default fallback to comprehensive daily business report
        return {"target": "daily_report", "payload": {}}

    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        self.status = "RUNNING"
        self.current_task = command
        self.last_run = datetime.now(timezone.utc)
        self.total_runs += 1

        # Check for persistent duplicate task in progress
        existing_task = db.query(AgentTask).filter(
            AgentTask.tenant_id == tenant_id,
            AgentTask.command == command,
            AgentTask.status.in_(["RUNNING", "PENDING"])
        ).first()

        if existing_task:
            self.status = "IDLE"
            return {
                "status": "DUPLICATE_TASK_SKIPPED",
                "message": f"Task already queued and active (Task ID: {existing_task.id}).",
                "task_id": existing_task.id
            }

        # Create persistent task in database
        task_record = AgentTask(
            tenant_id=tenant_id,
            agent_name=self.name,
            command=command,
            input_payload_json=json.dumps(payload),
            status="RUNNING",
            retry_count=0,
            cost_estimate_usd=0.01
        )
        db.add(task_record)
        db.commit()

        intent = self.parse_intent(command)
        target = intent["target"]
        merged_payload = {**intent.get("payload", {}), **payload}

        try:
            if target == "daily_report":
                # Synthesize cross-department operations overview
                crm_res = self.departments["crm_manager"].execute(tenant_id, "get_summary", {}, db)
                fin_res = self.departments["finance_monitor"].execute(tenant_id, "get_revenue", {}, db)
                qa_res = self.departments["compliance_qa"].execute(tenant_id, "audit", {}, db)

                result_data = {
                    "report_type": "DAILY_BUSINESS_PERFORMANCE",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "crm_overview": crm_res.get("summary", {}),
                    "financial_kpis": fin_res.get("metrics", {}),
                    "compliance_audit": {
                        "properties_flagged": qa_res.get("flagged_properties_count", 0),
                        "leads_flagged": qa_res.get("flagged_leads_count", 0)
                    }
                }
                msg = "Daily executive performance report synthesized successfully."
            else:
                agent = self.departments[target]
                result_data = agent.execute(tenant_id, command, merged_payload, db)
                msg = result_data.get("message", "Task executed successfully.")

            task_record.status = "COMPLETED"
            task_record.output_payload_json = json.dumps(result_data, default=str)
            db.commit()

            self.status = "IDLE"
            self.current_task = None
            return {
                "status": "SUCCESS",
                "message": msg,
                "task_id": task_record.id,
                "target_department": target,
                "result": result_data
            }

        except Exception as e:
            self.failed_runs += 1
            self.error_details = str(e)
            task_record.status = "FAILED"
            task_record.error_details = str(e)
            db.commit()
            self.status = "ERROR"
            return {
                "status": "FAILED",
                "message": f"Execution error in department [{target}]: {str(e)}",
                "task_id": task_record.id,
                "error": str(e)
            }

orchestrator = MasterOperationsOrchestrator()
