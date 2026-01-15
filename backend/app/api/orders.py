from fastapi import APIRouter
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory

"""
Orders Admin API

Purpose:
- View historical orders placed by customers
- Used by admins, auditors, and judges
- Read-only (orders are created by agents)
"""

router = APIRouter(
    prefix="/admin/orders",
    tags=["admin"]
)


@router.get("/")
def list_orders():
    """
    List all order history records.

    Admin-only endpoint.
    Returns:
    - customer_id
    - medicine_name
    - quantity
    - created_at
    """
    db = SessionLocal()
    try:
        orders = (
            db.query(OrderHistory)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )
        return orders
    finally:
        db.close()
