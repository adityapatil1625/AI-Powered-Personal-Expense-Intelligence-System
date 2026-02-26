from models import Transaction
from sqlalchemy import func
from models import Transaction


def create_transaction(db, transaction):
    new_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        transaction_date=transaction.transaction_date,
        merchant_name=transaction.merchant_name,
        category=transaction.category,
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

def get_expense_insights(db, user_id: str):

    total_spent = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id
    ).scalar()

    category_spending = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id
    ).group_by(
        Transaction.category
    ).all()

    highest_category = max(
        category_spending,
        key=lambda x: x[1]
    )[0] if category_spending else None

    return {
        "total_spent": total_spent,
        "category_breakdown": dict(category_spending),
        "highest_spending_category": highest_category
    }