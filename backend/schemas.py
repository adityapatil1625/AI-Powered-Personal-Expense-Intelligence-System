from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    transaction_date: date
    merchant_name: str
    category: str
    payment_mode: str