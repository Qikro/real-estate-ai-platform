from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.core.database import get_db
from app.models.entities import User, AgentTask
from app.schemas.schemas import OrchestratorCommandRequest, AgentTaskResponse
from app.api.deps import get_current_user
from app.agents.orchestrator import orchestrator

router = APIRouter(prefix="/agents", tags=["AI Agents"])

@router.get("")
def list_agents(current_user: User = Depends(get_current_user)):
    return {
        "status": "SUCCESS",
        "agents": orchestrator.get_agent_registry()
    }

@router.post("/command")
def dispatch_command(
    req: OrchestratorCommandRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = orchestrator.execute(
        tenant_id=current_user.tenant_id,
        command=req.command,
        payload={},
        db=db
    )
    return result

@router.post("/{agent_key}/run")
def run_specific_agent(
    agent_key: str,
    payload: Dict[str, Any] = {},
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if agent_key not in orchestrator.departments and agent_key != "orchestrator":
        raise HTTPException(status_code=404, detail="Agent department not found")

    if agent_key == "orchestrator":
        result = orchestrator.execute(
            tenant_id=current_user.tenant_id,
            command=payload.get("command", "Execute daily business report"),
            payload=payload,
            db=db
        )
    else:
        agent = orchestrator.departments[agent_key]
        cmd = payload.get("command", f"Run {agent.name}")
        result = agent.execute(
            tenant_id=current_user.tenant_id,
            command=cmd,
            payload=payload,
            db=db
        )
    return result

@router.get("/tasks", response_model=List[AgentTaskResponse])
def get_task_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(AgentTask).filter(
        AgentTask.tenant_id == current_user.tenant_id
    ).order_by(AgentTask.created_at.desc()).limit(limit).all()
    return tasks
