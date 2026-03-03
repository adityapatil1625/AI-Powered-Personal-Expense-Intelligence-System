"""Database models for Expense Intelligence."""
import uuid
from sqlalchemy import Column, String, Numeric, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Transaction(Base):
    """Transaction model for tracking expenses."""

    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    amount = Column(Numeric(10, 2))
    transaction_date = Column(Date)
    merchant_name = Column(String)
    category = Column(String)
    payment_mode = Column(String)


class MerchantCategoryMap(Base):
    """Merchant to category mapping for AI learning."""

    __tablename__ = "merchant_category_map"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_name = Column(String, unique=True)
    category = Column(String)


class Budget(Base):
    """Monthly budget tracking model."""

    __tablename__ = "budgets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    monthly_limit = Column(Float)
