from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    prediction = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    keywords = Column(Text, nullable=True)          # Comma-separated top keywords
    probabilities = Column(Text, nullable=True)     # JSON string of class probabilities
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "keywords": self.keywords.split(",") if self.keywords else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
