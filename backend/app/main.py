from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.chat import router as chat_router
from backend.app.api.admin import router as admin_router
from backend.app.api.orders import router as orders_router
from backend.app.api.customers import router as customers_router
from backend.app.api.decision_traces import router as decision_traces_router

from backend.app.db.seed_production import seed_production_data


app = FastAPI(
    title="Agentic Pharmacy Backend",
    version="1.0.0",
    description="AI-driven pharmacy automation system"
)

# -----------------------------
# Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in real prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Startup hooks
# -----------------------------
@app.on_event("startup")
def on_startup():
    seed_production_data()


# -----------------------------
# Health & Root
# -----------------------------
@app.get("/")
def root():
    return {"status": "Pharmacy backend running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "agentic-pharmacy",
        "environment": "production"
    }


# -----------------------------
# Routers
# -----------------------------
app.include_router(chat_router)
app.include_router(admin_router)
app.include_router(orders_router)
app.include_router(customers_router)
app.include_router(decision_traces_router)
