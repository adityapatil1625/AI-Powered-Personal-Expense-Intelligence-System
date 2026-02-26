from models import Transaction
from sqlalchemy import func
from models import Transaction
from datetime import datetime
from ai_engine import generate_insights
from category_ai import categorize_transaction


def create_transaction(db, transaction):

    auto_category = categorize_transaction(
        transaction.merchant_name
    )

    new_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        transaction_date=transaction.transaction_date,
        merchant_name=transaction.merchant_name,
        category=auto_category,
        payment_mode=transaction.payment_mode
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction
def get_user_transactions(db, user_id: str):
    return db.query(Transaction)\
        .filter(Transaction.user_id == user_id)\
        .all()

def get_expense_insights(db, user_id):

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    return generate_insights(transactions)