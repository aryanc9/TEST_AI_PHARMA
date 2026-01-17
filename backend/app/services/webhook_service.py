"""
Mock Webhook Service: Simulates warehouse integration
In production, this would POST to actual warehouse systems
"""

import json
from datetime import datetime
from app.db.database import SessionLocal
from app.db.models import Order, Customer


class WebhookPayload:
    """Standardized webhook payload for warehouse"""
    
    def __init__(self, order_id: int, customer_id: int, medicines: list):
        self.order_id = order_id
        self.customer_id = customer_id
        self.medicines = medicines
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            "event": "order.created",
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "medicines": self.medicines,
            "timestamp": self.timestamp,
            "priority": "standard"
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), default=str)


async def trigger_warehouse_webhook(order_id: int, medicines: list, customer_id: int) -> dict:
    """
    Mock webhook trigger
    In production: POST to https://warehouse.company.com/api/orders
    Status codes: 200 = success, 4xx/5xx = retry
    """
    payload = WebhookPayload(order_id, customer_id, medicines)
    
    # MOCK: Print webhook payload
    print(f"🚀 WEBHOOK TRIGGERED: {payload.to_json()}")
    
    # In production, this would be:
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://warehouse.company.com/api/orders",
    #         json=payload.to_dict(),
    #         headers={"X-API-KEY": settings.WAREHOUSE_API_KEY}
    #     )
    #     return {"status": response.status_code, "order_id": order_id}
    
    return {
        "status": 200,
        "order_id": order_id,
        "message": "Webhook delivered to warehouse",
        "payload": payload.to_dict()
    }


def send_order_confirmation(customer_id: int, order_id: int, medicines: list) -> dict:
    """
    Mock order confirmation: Email + SMS
    In production: Integrate Twilio/SendGrid
    """
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        
        if not customer:
            return {"status": "failed", "reason": "Customer not found"}
        
        # Build confirmation message
        medicine_list = "\n".join([
            f"  • {m['name']} x{m['quantity']} ({m.get('dosage', 'N/A')})"
            for m in medicines
        ])
        
        email_body = f"""
Thank you for your order!

Order ID: {order_id}
Medicines:
{medicine_list}

Pickup at your nearest pharmacy within 4 hours.

Thank you for trusting AI Pharmacy!
"""
        
        sms_body = f"Order #{order_id} confirmed. Pickup in 4 hours. Ref: {order_id}"
        
        # MOCK: Print confirmation
        print(f"\n📧 EMAIL SENT to {customer.email or 'N/A'}")
        print(f"Subject: Order #{order_id} Confirmed")
        print(email_body)
        
        print(f"\n📱 SMS SENT to {customer.phone or 'N/A'}")
        print(f"Message: {sms_body}")
        
        return {
            "status": "sent",
            "order_id": order_id,
            "email": customer.email,
            "phone": customer.phone,
            "message": "Confirmation sent via email and SMS"
        }
    finally:
        db.close()
