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