from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.blnibaxszoicsinoehvs:CJjXxpOLvVPovldB@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
print(DATABASE_URL)
print("DATABASE URL USED:", DATABASE_URL)