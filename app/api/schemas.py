from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class KeywordAttribution(BaseModel):
    word: str
    weight: float

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Leave application explanation text")

class AnalyzeResponse(BaseModel):
    id: int
    text: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    keywords: List[str]
    attributions: List[KeywordAttribution]
    risk_level: str
    recommendation: str
    created_at: str

class BatchAnalyzeRequest(BaseModel):
    applications: List[str] = Field(..., min_length=1, max_length=100)

class BatchAnalyzeResponse(BaseModel):
    total_processed: int
    results: List[AnalyzeResponse]

class HistoryItem(BaseModel):
    id: int
    text: str
    prediction: str
    confidence: float
    keywords: List[str]
    created_at: str

class StatsResponse(BaseModel):
    total: int
    genuine: int
    suspicious: int
    emotional: int
    model_accuracy: float
    suspicious_rate: float
    genuine_rate: float
    emotional_rate: float

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    model_loaded: bool
    model_accuracy: float
    classes: List[str]
