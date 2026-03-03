from fastapi import FastAPI, Depends, Body
from sqlalchemy.orm import Session
from fastapi import Body
from auth import hash_password, verify_password, create_access_token, get_current_user
from crud import (
    create_transaction,
    get_user_transactions,
    get_expense_insights,
    generate_chat_response,
    set_budget  
)

from database import SessionLocal, engine
from schemas import TransactionCreate, UserCreate, UserLogin
from crud import create_transaction, get_user_transactions, get_expense_insights
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User

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


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            return {"error": "Email already registered"}

        new_user = User(
            email=user.email,
            hashed_password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        print(f"Registration error: {str(e)}")
        return {"error": f"Registration failed: {str(e)}"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            return {"error": "Invalid credentials"}

        if not verify_password(user.password, db_user.hashed_password):
            return {"error": "Invalid credentials"}

        access_token = create_access_token({"sub": db_user.id})

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login error: {str(e)}")
        return {"error": f"Login failed: {str(e)}"}



@app.post("/transactions")
def add_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction.user_id = current_user.id
    create_transaction(db, transaction)
    return {"message": "Transaction added successfully"}

@app.get("/transactions")
def fetch_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = get_user_transactions(db, current_user.id)
    return transactions

@app.get("/insights")
def insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_expense_insights(db, current_user.id)

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

@app.post("/chat")
def chat_with_ai(
    message: str = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    insights = get_expense_insights(db, current_user.id)
    response = generate_chat_response(message, insights)
    return {"response": response}


@app.post("/budget")
def create_budget(
    limit: float = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return set_budget(db, current_user.id, limit)