"""Budget management service."""
import uuid
from sqlalchemy.orm import Session
from app.models.models import Budget


def set_budget(db: Session, user_id: str, monthly_limit: float) -> dict:
    """Create or update user budget."""
    existing = db.query(Budget).filter(
        Budget.user_id == user_id
    ).first()

    if existing:
        existing.monthly_limit = monthly_limit
    else:
        new_budget = Budget(
            id=str(uuid.uuid4()),
            user_id=user_id,
            monthly_limit=monthly_limit
        )
        db.add(new_budget)

    db.commit()
    return {"message": "Budget saved successfully"}
