import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Analysis

# Use in-memory SQLite for test isolation
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_create_and_retrieve_analysis(db_session):
    record = Analysis(
        text="Suffering from severe migraine headache.",
        prediction="Genuine",
        confidence=0.985,
        keywords="migraine,headache,severe",
        probabilities='{"Genuine": 0.985, "Emotional": 0.01, "Suspicious": 0.005}'
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    assert record.id is not None
    fetched = db_session.query(Analysis).filter(Analysis.id == record.id).first()
    assert fetched is not None
    assert fetched.prediction == "Genuine"
    assert fetched.confidence == 0.985
    assert "migraine" in fetched.keywords

def test_delete_analysis(db_session):
    record = Analysis(
        text="Alien invasion in my backyard.",
        prediction="Suspicious",
        confidence=0.99,
        keywords="alien,backyard"
    )
    db_session.add(record)
    db_session.commit()
    record_id = record.id

    db_session.delete(record)
    db_session.commit()

    deleted = db_session.query(Analysis).filter(Analysis.id == record_id).first()
    assert deleted is None
