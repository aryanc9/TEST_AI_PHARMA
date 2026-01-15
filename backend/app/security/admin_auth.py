import os
from fastapi import Header, HTTPException, status

"""
Admin Authentication Dependency

- Enforces admin access using a static API key
- Designed for backend/admin routes only
- Works with FastAPI dependency injection
- Safe for Docker, Railway, and local dev
"""

# Load admin key from environment (required in production)
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "dev-admin-key")


def admin_auth(x_admin_key: str = Header(None)):
    """
    Validates admin access using X-ADMIN-KEY header.

    Header required:
        X-ADMIN-KEY: <ADMIN_API_KEY>

    Raises:
        HTTPException(401) if key is missing or invalid
    """
    if not x_admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-ADMIN-KEY header missing"
        )

    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    # Explicit success (important for clarity)
    return True
