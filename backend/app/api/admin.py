from fastapi import APIRouter, Depends
from backend.app.security.admin_auth import admin_auth

"""
Admin Router

Purpose:
- Acts as the security gate for all admin-level routes
- Applies admin authentication globally
- Does NOT contain business logic

All admin resources (medicines, orders, customers, refill alerts, traces)
must be mounted AFTER this router in main.py
"""

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(admin_auth)]
)
