"""Budget Management API routes."""
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import User
from app.services.budget_service import set_budget

router = APIRouter(prefix="/budget", tags=["Budget"])


@router.post("/")
def create_budget(
    limit: float = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set or update monthly budget limit."""
    return set_budget(db, current_user.id, limit)
