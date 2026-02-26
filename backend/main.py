from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import TransactionCreate
from crud import create_transaction, get_user_transactions, get_expense_insights

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Expense Intelligence Running"}


@app.post("/transactions")
def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    create_transaction(db, transaction)
    return {"message": "Transaction added successfully"}

@app.get("/transactions/{user_id}")
def fetch_transactions(user_id: str, db: Session = Depends(get_db)):
    transactions = get_user_transactions(db, user_id)
    return transactions

@app.get("/insights/{user_id}")
def expense_insights(user_id: str, db: Session = Depends(get_db)):
    insights = get_expense_insights(db, user_id)
    return insights

@app.get("/insights/{user_id}")
def expense_insights(user_id: str, db: Session = Depends(get_db)):
    return get_expense_insights(db, user_id)