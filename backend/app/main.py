from fastapi import FastAPI
from backend.app.db.database import engine
from backend.app.db import models
from backend.app.api import medicines, customers, orders
from backend.app.api.chat import router as chat_router
from backend.app.api.admin import router as admin_router
from backend.app.api.health import router as health_router
from backend.app.api import chat, admin
from backend.app.config import ENV

app = FastAPI(
    title="Agentic AI Pharmacy",
    debug=ENV == "development"
)
app.include_router(chat_router)


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic AI Pharmacy System")

app.include_router(medicines.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(admin_router) 

@app.get("/")
def health_check():
    return {"status": "Pharmacy backend running"}
