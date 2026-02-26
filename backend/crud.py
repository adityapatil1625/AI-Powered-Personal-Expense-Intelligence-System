from models import Transaction
from sqlalchemy import func
from models import Transaction
from datetime import datetime


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

def get_expense_insights(db, user_id):

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    if not transactions:
        return {"message": "No transactions found"}

    # ✅ Total Spending
    total_spent = float(sum(t.amount for t in transactions))

    # ✅ Category Breakdown
    category_data = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .filter(Transaction.user_id == user_id)
        .group_by(Transaction.category)
        .all()
    )

    category_breakdown = {
        category: float(amount)
        for category, amount in category_data
    }

    highest_category = max(
        category_breakdown,
        key=category_breakdown.get
    )

    # ✅ Monthly Spending Trend
    monthly_data = (
        db.query(
            func.date_trunc(
                'month',
                Transaction.transaction_date
            ),
            func.sum(Transaction.amount)
        )
        .filter(Transaction.user_id == user_id)
        .group_by(
            func.date_trunc(
                'month',
                Transaction.transaction_date
            )
        )
        .all()
    )

    monthly_trend = {
        str(month.date()): float(amount)
        for month, amount in monthly_data
    }

    # ✅ Average Daily Spend
    unique_days = len(
        set(t.transaction_date for t in transactions)
    )

    avg_daily_spend = total_spent / unique_days

    # ✅ Smart Warning
    warning = None
    if category_breakdown[highest_category] > total_spent * 0.5:
        warning = f"High spending detected in {highest_category}"

    return {
        "total_spent": total_spent,
        "highest_spending_category": highest_category,
        "category_breakdown": category_breakdown,
        "monthly_trend": monthly_trend,
        "average_daily_spend": round(avg_daily_spend, 2),
        "warning": warning
    }