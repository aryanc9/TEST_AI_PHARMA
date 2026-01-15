from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer, Medicine


def seed_production_data():
    db = SessionLocal()

    try:
        # -------------------------
        # Seed customer
        # -------------------------
        customer = db.query(Customer).first()
        if not customer:
            customer = Customer(
                id=1,
                name="Test User",
                phone="9999999999"
            )
            db.add(customer)
            db.commit()

        # -------------------------
        # Seed medicines
        # -------------------------
        if db.query(Medicine).count() == 0:
            db.add_all([
                Medicine(
                    name="Paracetamol 500mg",
                    stock_quantity=100,
                    prescription_required=False
                ),
                Medicine(
                    name="Amoxicillin 500mg",
                    stock_quantity=50,
                    prescription_required=True
                )
            ])
            db.commit()

    finally:
        db.close()
