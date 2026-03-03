"""Insights and Analytics API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import User
from app.services.insights_service import get_expense_insights

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/")
def fetch_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive financial insights for the current user."""
    return get_expense_insights(db, current_user.id)
