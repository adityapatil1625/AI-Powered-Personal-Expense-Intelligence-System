"""Transaction API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import User
from app.schemas.schemas import TransactionCreate, TransactionResponse
from app.services.transaction_service import (
    create_transaction,
    get_user_transactions
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=dict)
def add_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new transaction for the current user."""
    # Create a copy of transaction data and add user_id
    transaction_data = transaction.dict()
    transaction_data['user_id'] = current_user.id
    
    # Create transaction with user_id included
    response_transaction = create_transaction(
        db, 
        TransactionCreate(**transaction_data)
    )
    
    return {"message": "Transaction added successfully", "id": response_transaction.id}


@router.get("/", response_model=list)
def fetch_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all transactions for the current user."""
    transactions = get_user_transactions(db, current_user.id)
    return [
        {
            "id": t.id,
            "amount": float(t.amount),
            "date": t.transaction_date.isoformat(),
            "merchant": t.merchant_name,
            "category": t.category,
            "payment_mode": t.payment_mode,
        }
        for t in transactions
    ]
