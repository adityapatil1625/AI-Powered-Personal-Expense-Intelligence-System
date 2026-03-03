
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres.blnibaxszoicsinoehvs:CJjXxpOLvVPovldB@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

# Create engine with SSL mode required for Supabase
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require",
    },
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() 