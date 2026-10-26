import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BatchAnalyzeRequest,
    BatchAnalyzeResponse,
    KeywordAttribution
)
from app.db.session import get_db
from app.db.models import Analysis
from app.ml.engine import classifier

router = APIRouter(prefix="", tags=["Inference & Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_201_CREATED)
def analyze_application(req: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Classify a single leave application, extract keyword attributions, and store the audit record.
    """
    text = req.text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application text cannot be empty."
        )

    try:
        clf = classifier()
        result = clf.predict(text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference pipeline error: {str(e)}"
        )

    # Persist record to database
    record = Analysis(
        text=text,
        prediction=result["prediction"],
        confidence=result["confidence"],
        keywords=",".join(result["keywords"]),
        probabilities=json.dumps(result["probabilities"]),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return AnalyzeResponse(
        id=record.id,
        text=record.text,
        prediction=record.prediction,
        confidence=record.confidence,
        probabilities=result["probabilities"],
        keywords=result["keywords"],
        attributions=[KeywordAttribution(**a) for a in result["attributions"]],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"],
        created_at=record.created_at.isoformat() if record.created_at else "",
    )

@router.post("/batch", response_model=BatchAnalyzeResponse, status_code=status.HTTP_200_OK)
def batch_analyze_applications(req: BatchAnalyzeRequest, db: Session = Depends(get_db)):
    """
    Classify multiple leave applications simultaneously with transactional persistence.
    """
    if not req.applications:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application list cannot be empty."
        )

    clf = classifier()
    responses: List[AnalyzeResponse] = []

    for app_text in req.applications:
        text = app_text.strip()
        if not text:
            continue

        result = clf.predict(text)
        record = Analysis(
            text=text,
            prediction=result["prediction"],
            confidence=result["confidence"],
            keywords=",".join(result["keywords"]),
            probabilities=json.dumps(result["probabilities"]),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        responses.append(
            AnalyzeResponse(
                id=record.id,
                text=record.text,
                prediction=record.prediction,
                confidence=record.confidence,
                probabilities=result["probabilities"],
                keywords=result["keywords"],
                attributions=[KeywordAttribution(**a) for a in result["attributions"]],
                risk_level=result["risk_level"],
                recommendation=result["recommendation"],
                created_at=record.created_at.isoformat() if record.created_at else "",
            )
        )

    return BatchAnalyzeResponse(
        total_processed=len(responses),
        results=responses
    )
