"""Shared pytest fixtures and test environment setup."""
import os
from pathlib import Path

TEST_DB_PATH = Path(__file__).resolve().parents[1] / "test_expense_intelligence.db"

os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB_PATH.as_posix()}")
os.environ.setdefault("INIT_DB_ON_STARTUP", "True")
os.environ.setdefault("DEBUG", "False")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
