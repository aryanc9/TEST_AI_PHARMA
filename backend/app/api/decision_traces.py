from fastapi import APIRouter
from backend.app.db.database import SessionLocal
from backend.app.db.models import DecisionTrace

"""
Decision Traces Admin API

Purpose:
- Expose agent decision traces for judges and auditors
- Show how the system reasoned step-by-step
- Read-only by design
"""

router = APIRouter(
    prefix="/admin/decision-traces",
    tags=["admin"]
)


@router.get("/")
def list_decision_traces(limit: int = 50):
    """
    List recent decision traces.

    Query params:
    - limit: number of traces to return (default 50)
    """
    db = SessionLocal()
    try:
        traces = (
            db.query(DecisionTrace)
            .order_by(DecisionTrace.created_at.desc())
            .limit(limit)
            .all()
        )
        return traces
    finally:
        db.close()


@router.get("/{trace_id}")
def get_decision_trace(trace_id: int):
    """
    Get a single decision trace by ID.
    """
    db = SessionLocal()
    try:
        trace = (
            db.query(DecisionTrace)
            .filter(DecisionTrace.id == trace_id)
            .first()
        )

        if not trace:
            return {"error": "Decision trace not found"}

        return trace
    finally:
        db.close()
