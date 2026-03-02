from fastapi import FastAPI, Depends, Body
from sqlalchemy.orm import Session
from fastapi import Body
from crud import (
    create_transaction,
    get_user_transactions,
    get_expense_insights,
    generate_chat_response,
    set_budget  
)

from database import SessionLocal, engine
from schemas import TransactionCreate
from crud import create_transaction, get_user_transactions, get_expense_insights
from fastapi.middleware.cors import CORSMiddleware
from models import Base

Base.metadata.create_all(bind=engine)

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

@app.post("/learn-category")
def learn(
    merchant_name: str,
    category: str,
    db: Session = Depends(get_db)
):
    learn_category(db, merchant_name, category)

    return {"message": "AI learned successfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/{user_id}")
def chat_with_ai(user_id: str, message: str = Body(...), db: Session = Depends(get_db)):

    insights = get_expense_insights(db, user_id)

    response = generate_chat_response(message, insights)

    return {"response": response}


@app.post("/budget/{user_id}")
def create_budget(user_id: str, limit: float = Body(...), db: Session = Depends(get_db)):
    return set_budget(db, user_id, limit)