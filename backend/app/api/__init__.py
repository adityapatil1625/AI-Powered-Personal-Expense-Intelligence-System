"""API router exports."""

from app.api import ai_routes, auth_routes, budget_routes, insights_routes, transaction_routes

__all__ = [
    "ai_routes",
    "auth_routes",
    "budget_routes",
    "insights_routes",
    "transaction_routes",
]
