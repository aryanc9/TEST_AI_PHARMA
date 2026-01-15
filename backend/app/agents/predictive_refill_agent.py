from datetime import datetime
from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def predictive_refill_agent(state: PharmacyState) -> PharmacyState:
    """
    Predictive Refill Agent

    Responsibilities:
    - Analyze order history
    - Generate refill alerts
    - Append insights without mutating core state
    """

    db = SessionLocal()
    customer_id = state["customer"]["id"]

    alerts = []

    try:
        history = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )

        latest_by_medicine = {}

        for record in history:
            if record.medicine_name not in latest_by_medicine:
                latest_by_medicine[record.medicine_name] = record

        for medicine, record in latest_by_medicine.items():
            days_since = (datetime.utcnow() - record.created_at).days

            if days_since >= 1:
                alerts.append({
                    "medicine": medicine,
                    "last_order_date": record.created_at.isoformat(),
                    "days_since_last_order": days_since,
                    "message": f"Likely running low on {medicine}"
                })

        state["meta"]["refill_alerts"] = alerts

        state["decision_trace"].append({
            "agent": "predictive_refill_agent",
            "input": {"customer_id": customer_id},
            "reasoning": f"Analyzed order history, generated {len(alerts)} alerts",
            "decision": "alerts_generated",
            "output": alerts
        })

        return state

    finally:
        db.close()
