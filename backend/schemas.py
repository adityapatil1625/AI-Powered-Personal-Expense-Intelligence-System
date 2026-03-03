from pydantic import BaseModel, EmailStr
from datetime import date

class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    transaction_date: date
    merchant_name: str
    category: str
    payment_mode: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str