"""Application configuration and environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.blnibaxszoicsinoehvs:CJjXxpOLvVPovldB@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
    )

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # API
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    CORS_ORIGINS: list = [
        os.getenv("CORS_ORIGIN", "http://localhost:5173")
    ]

    # App
    APP_NAME: str = "Expense Intelligence"
    APP_version: str = "1.0.0"


settings = Settings()
