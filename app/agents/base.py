from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import json
from sqlalchemy.orm import Session
from app.models.entities import AgentTask, ApprovalRequest, AuditLog

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.status = "IDLE"
        self.last_run: Optional[datetime] = None
        self.total_runs = 0
        self.failed_runs = 0
        self.total_cost_usd = 0.0
        self.current_task: Optional[str] = None
        self.error_details: Optional[str] = None

    @property
    def success_rate(self) -> float:
        if self.total_runs == 0:
            return 100.0
        return round(((self.total_runs - self.failed_runs) / self.total_runs) * 100.0, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "status": self.status,
            "current_task": self.current_task or "None",
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "total_runs": self.total_runs,
            "success_rate": self.success_rate,
            "cost_usd": round(self.total_cost_usd, 4),
            "error_details": self.error_details,
            "next_scheduled_run": "Continuous / Event-driven"
        }

    def log_audit(self, db: Session, tenant_id: str, action: str, entity_type: str, entity_id: str, details: dict):
        log = AuditLog(
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            change_details_json=json.dumps(details, default=str),
            ip_address="internal-agent-bus"
        )
        db.add(log)
        db.commit()

    @abstractmethod
    def execute(self, tenant_id: str, command: str, payload: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Core execution logic implemented by specialized agents"""
        pass
