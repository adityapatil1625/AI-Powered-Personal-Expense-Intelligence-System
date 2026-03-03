"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class TransactionCreate(BaseModel):
    """Schema for creating a transaction."""

    user_id: Optional[str] = None
    amount: float
    transaction_date: date
    merchant_name: str
    category: str
    payment_mode: str


class TransactionResponse(TransactionCreate):
    """Schema for transaction response."""

    id: str


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str


class BudgetCreate(BaseModel):
    """Schema for creating/updating budget."""

    monthly_limit: float
