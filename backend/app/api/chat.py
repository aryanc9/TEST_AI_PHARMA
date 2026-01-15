from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.app.graph.pharmacy_workflow import run_workflow
from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    approved: bool
    reply: str
    order_id: Optional[int] = None


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    db = SessionLocal()

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == request.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        final_state = run_workflow(
            customer_id=customer.id,
            message=request.message
        )

        safety = final_state.get("safety", {})
        execution = final_state.get("execution", {})

        if not safety.get("approved"):
            return ChatResponse(
                approved=False,
                reply="Request blocked by safety rules"
            )

        return ChatResponse(
            approved=True,
            reply="Order placed successfully",
            order_id=execution.get("order_id")
        )

    finally:
        db.close()
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.app.graph.pharmacy_workflow import run_workflow
from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer

"""
Chat API

Public endpoint used by customers.
This is the primary entry point into the agentic system.
"""

router = APIRouter(prefix="/chat", tags=["chat"])


# ----------- Schemas -----------

class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    approved: bool
    reply: str
    order_id: Optional[int] = None


# ----------- Endpoint -----------

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main conversational endpoint.

    Flow:
    1. Validate customer
    2. Run agentic pharmacy workflow
    3. Return human-friendly response
    """

    db = SessionLocal()

    try:
        # Validate customer
        customer = (
            db.query(Customer)
            .filter(Customer.id == request.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # Run agentic workflow
        final_state = run_workflow(
            message=request.message,
            customer_id=customer.id
        )

        safety = final_state.get("safety", {})
        execution = final_state.get("execution", {})

        # Safety blocked
        if not safety.get("approved", False):
            return ChatResponse(
                approved=False,
                reply="Your request could not be processed due to safety rules.",
                order_id=None
            )

        # Success
        return ChatResponse(
            approved=True,
            reply="Your order has been placed successfully.",
            order_id=execution.get("order_id")
        )

    finally:
        db.close()
