"""Database connection and session management."""
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.models.models import Base


def _get_connect_args(database_url: str) -> dict:
    """Use SSL for remote DBs while keeping local development simple."""
    local_hosts = ("@localhost", "@127.0.0.1", "@db:")
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    if any(host in database_url for host in local_hosts):
        return {}
    return {"sslmode": "require"}

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_get_connect_args(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database and create all tables."""
    last_error = None

    for attempt in range(1, settings.DB_INIT_MAX_RETRIES + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as exc:
            last_error = exc
            if attempt == settings.DB_INIT_MAX_RETRIES:
                raise
            time.sleep(settings.DB_INIT_RETRY_DELAY_SECONDS)

    if last_error:
        raise last_error
