from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.schemas import HistoryItem
from app.db.session import get_db
from app.db.models import Analysis

router = APIRouter(prefix="/history", tags=["Audit History"])

@router.get("", response_model=List[HistoryItem])
def get_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    category: Optional[str] = Query(None, description="Optional filter by Genuine, Suspicious, Emotional"),
    db: Session = Depends(get_db)
):
    """
    Fetch historical leave analysis audit records with pagination and category filtering.
    """
    query = db.query(Analysis)
    if category:
        query = query.filter(Analysis.prediction == category)

    records = (
        query.order_by(Analysis.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        HistoryItem(
            id=r.id,
            text=r.text,
            prediction=r.prediction,
            confidence=r.confidence,
            keywords=r.keywords.split(",") if r.keywords else [],
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
        )
        for r in records
    ]

@router.delete("/{record_id}", status_code=status.HTTP_200_OK)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific historical record by ID.
    """
    record = db.query(Analysis).filter(Analysis.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis record #{record_id} not found."
        )
    db.delete(record)
    db.commit()
    return {"message": f"Record #{record_id} deleted successfully."}

@router.delete("", status_code=status.HTTP_200_OK)
def clear_all_history(db: Session = Depends(get_db)):
    """
    Clear all records from audit history.
    """
    count = db.query(Analysis).delete()
    db.commit()
    return {"message": f"Cleared {count} audit records."}
