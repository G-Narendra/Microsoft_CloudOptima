"""Local authentication and RBAC for Streamlit dashboard."""

from __future__ import annotations

from typing import Final

USERS: Final[dict[str, dict[str, str]]] = {
    "admin": {
        "password": "password",
        "role": "admin",
        "name": "Admin User",
    },
    "reviewer": {
        "password": "password",
        "role": "reviewer",
        "name": "Reviewer User"
    },
    "viewer": {
        "password": "password",
        "role": "viewer",
        "name": "Viewer User"
    }
}

def authenticate(username: str, password: str) -> dict[str, str] | None:
    """Authenticate a user and return their profile if successful."""
    if username in USERS and USERS[username]["password"] == password:
        return {
            "username": username,
            "role": USERS[username]["role"],
            "name": USERS[username]["name"]
        }
    return None

def can_approve(role: str) -> bool:
    """Check if the role has permission to approve deployments."""
    return role in ("admin", "reviewer")

def can_deploy(role: str) -> bool:
    """Check if the role has permission to trigger a deployment."""
    return role in ("admin", "reviewer")
