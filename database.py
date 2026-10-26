from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./excusesense.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Analysis(Base):
    """Stores every leave application analyzed by the system."""
    __tablename__ = "analyses"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text       = Column(String,  nullable=False)
    prediction = Column(String,  nullable=False)          # Genuine | Suspicious | Emotional
    confidence = Column(Float,   nullable=False)
    keywords   = Column(String,  nullable=True)           # comma-separated
    probabilities = Column(String, nullable=True)        # JSON string of probabilities
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables on import
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
