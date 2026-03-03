"""AI Chat API routes."""
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import User
from app.services.insights_service import get_expense_insights
from app.services.ai_service import generate_chat_response

router = APIRouter(prefix="/chat", tags=["AI"])


@router.post("/")
def chat_with_ai(
    message: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI about expenses and financial insights."""
    insights = get_expense_insights(db, current_user.id)
    response = generate_chat_response(message, insights)
    return {"response": response}
