"""
ExcuseSense FastAPI Backend
Run with: uvicorn backend:app --reload --port 8000
"""
import re
from datetime import datetime
from typing import List

import joblib
import numpy as np
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Analysis, Base, engine, get_db

# ── Create tables ──────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ExcuseSense API",
    description="AI-powered leave application classifier backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load ML artifacts ──────────────────────────────────────────────────────────
try:
    model      = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    MODEL_ACC  = float(open("metrics.txt").read().strip())
except FileNotFoundError as e:
    raise RuntimeError(f"ML artifact missing — run train_model.py first. ({e})")


# ── Helpers ────────────────────────────────────────────────────────────────────
def preprocess(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower())


def top_keywords(raw: str, class_idx: int, n: int = 5) -> List[str]:
    coef = model.coef_[class_idx]
    seen, scored = set(), []
    for w in preprocess(raw).split():
        if w in seen or w not in vectorizer.vocabulary_:
            continue
        seen.add(w)
        scored.append((w, coef[vectorizer.vocabulary_[w]]))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [w for w, s in scored if s > 0][:n]


# ── Pydantic schemas ───────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    id:            int
    prediction:    str
    confidence:    float
    keywords:      List[str]
    probabilities: dict
    timestamp:     str


class HistoryItem(BaseModel):
    id:         int
    text:       str
    prediction: str
    confidence: float
    keywords:   List[str]
    created_at: str


class StatsResponse(BaseModel):
    total:          int
    genuine:        int
    suspicious:     int
    emotional:      int
    model_accuracy: float


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "message":  "ExcuseSense API is running 🚀",
        "version":  "1.0.0",
        "accuracy": MODEL_ACC,
    }


@app.post("/analyze", response_model=AnalyzeResponse, tags=["ML"])
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    """Classify a leave application and persist the result to the database."""
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    clean     = preprocess(text)
    vec_in    = vectorizer.transform([clean])
    prediction = model.predict(vec_in)[0]
    probs     = model.predict_proba(vec_in)[0]
    class_idx = list(model.classes_).index(prediction)
    confidence = float(probs[class_idx])
    keywords  = top_keywords(text, class_idx)
    proba_map = {cls: round(float(p), 4) for cls, p in zip(model.classes_, probs)}

    # Persist
    record = Analysis(
        text       = text,
        prediction = prediction,
        confidence = round(confidence, 4),
        keywords   = ",".join(keywords),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return AnalyzeResponse(
        id            = record.id,
        prediction    = prediction,
        confidence    = round(confidence, 4),
        keywords      = keywords,
        probabilities = proba_map,
        timestamp     = record.created_at.isoformat(),
    )


@app.get("/history", response_model=List[HistoryItem], tags=["Database"])
def get_history(limit: int = 30, db: Session = Depends(get_db)):
    """Fetch the most recent analyses from the database."""
    records = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        HistoryItem(
            id         = r.id,
            text       = r.text,
            prediction = r.prediction,
            confidence = r.confidence,
            keywords   = r.keywords.split(",") if r.keywords else [],
            created_at = r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
        for r in records
    ]


@app.get("/stats", response_model=StatsResponse, tags=["Database"])
def get_stats(db: Session = Depends(get_db)):
    """Return aggregate counts from the database."""
    def count(label):
        return db.query(Analysis).filter(Analysis.prediction == label).count()

    return StatsResponse(
        total          = db.query(Analysis).count(),
        genuine        = count("Genuine"),
        suspicious     = count("Suspicious"),
        emotional      = count("Emotional"),
        model_accuracy = MODEL_ACC,
    )


@app.delete("/history/{record_id}", tags=["Database"])
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a specific analysis record."""
    record = db.query(Analysis).filter(Analysis.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")
    db.delete(record)
    db.commit()
    return {"message": f"Record #{record_id} deleted successfully."}


@app.delete("/history", tags=["Database"])
def clear_history(db: Session = Depends(get_db)):
    """Delete ALL records from the database."""
    db.query(Analysis).delete()
    db.commit()
    return {"message": "All history cleared."}
