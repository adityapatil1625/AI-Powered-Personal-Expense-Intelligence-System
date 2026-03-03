"""Transaction management service."""
from sqlalchemy.orm import Session
from app.models.models import Transaction
from app.schemas.schemas import TransactionCreate


def create_transaction(
    db: Session,
    transaction: TransactionCreate
) -> Transaction:
    """Create a new transaction."""
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_user_transactions(
    db: Session,
    user_id: str
) -> list[Transaction]:
    """Get all transactions for a user."""
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )
