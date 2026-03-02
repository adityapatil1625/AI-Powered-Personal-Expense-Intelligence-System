from sqlalchemy import Column, String, Numeric, Date, Float
from sqlalchemy.orm import declarative_base
import uuid
from database import Base

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

class MerchantCategoryMap(Base):
    __tablename__ = "merchant_category_map"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    merchant_name = Column(String, unique=True)
    category = Column(String)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    monthly_limit = Column(Float)