from sqlalchemy import Column, String, Numeric, Date
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String)
    amount = Column(Numeric)
    transaction_date = Column(Date)
    merchant_name = Column(String)
    category = Column(String)
    payment_mode = Column(String)