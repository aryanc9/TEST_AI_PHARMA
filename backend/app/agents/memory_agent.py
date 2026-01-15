from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def memory_agent(state: PharmacyState) -> PharmacyState:
    """
    Memory Agent

    Responsibilities:
    - Fetch customer order history
    - Provide context for downstream agents
    - NEVER overwrite state keys
    """

    db = SessionLocal()
    customer_id = state["customer"]["id"]

    try:
        history = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .limit(5)
            .all()
        )

        history_payload = [
            {
                "medicine": h.medicine_name,
                "quantity": h.quantity,
                "date": h.created_at.isoformat()
            }
            for h in history
        ]

        # Store in meta only
        state["meta"]["customer_history"] = history_payload

        # Judge-visible trace
        state["decision_trace"].append({
            "agent": "memory_agent",
            "input": {"customer_id": customer_id},
            "reasoning": f"Fetched {len(history_payload)} previous orders",
            "decision": "context_provided",
            "output": history_payload
        })

        return state

    finally:
        db.close()
