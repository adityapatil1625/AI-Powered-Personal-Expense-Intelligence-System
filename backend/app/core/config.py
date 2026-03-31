"""Application configuration and environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://expenseuser:securepassword@localhost:5432/expense_intelligence"
    )

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # API
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    _cors_raw = os.getenv("CORS_ORIGIN", "http://localhost:5173")
    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in _cors_raw.split(",") if origin.strip()
    ]
    CORS_ORIGIN_REGEX: str = os.getenv(
        "CORS_ORIGIN_REGEX",
        r"^http://(localhost|127\.0\.0\.1):\d+$"
    )

    # App
    APP_NAME: str = "Expense Intelligence"
    APP_VERSION: str = "1.0.0"


settings = Settings()
