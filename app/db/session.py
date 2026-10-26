from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.db.models import Base

# Configure engine arguments for SQLite vs PostgreSQL
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Ensure backward compatible schema migration for SQLite
    if settings.DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            try:
                # Check if probabilities column exists
                res = conn.execute(text("PRAGMA table_info(analyses);")).fetchall()
                col_names = [r[1] for r in res]
                if "probabilities" not in col_names and len(col_names) > 0:
                    conn.execute(text("ALTER TABLE analyses ADD COLUMN probabilities TEXT;"))
                    conn.commit()
            except Exception:
                pass

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
