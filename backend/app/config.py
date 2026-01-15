import os

# Environment
ENV = os.getenv("ENV", "development")

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./pharmacy.db"
)

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = ENV == "development"

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Safety
MAX_QTY_PER_ORDER = int(os.getenv("MAX_QTY_PER_ORDER", 30))

# Scheduler
REFILL_INTERVAL_SECONDS = int(
    os.getenv("REFILL_INTERVAL_SECONDS", 3600)
)

# -------------------------------------------------------------------
# Observability
# -------------------------------------------------------------------

ENABLE_DECISION_TRACE = os.getenv(
    "ENABLE_DECISION_TRACE", "true"
).lower() == "true"


# --------------------
