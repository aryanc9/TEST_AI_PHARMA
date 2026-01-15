from fastapi import APIRouter
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine

"""
Medicines Admin API

Purpose:
- View current inventory
- Acts as source of truth for stock and prescription rules
- Read-only (mutations handled by agents)
"""

router = APIRouter(
    prefix="/admin/medicines",
    tags=["admin"]
)


@router.get("/")
def list_medicines():
    """
    List all medicines in inventory.

    Admin-only endpoint.
    """
    db = SessionLocal()
    try:
        medicines = db.query(Medicine).all()
        return medicines
    finally:
        db.close()
