from fastapi import APIRouter
from app.api.schemas import HealthResponse
from app.core.config import settings
from app.ml.engine import classifier

router = APIRouter(prefix="", tags=["System Health"])

@router.get("/health", response_model=HealthResponse)
def healthcheck():
    """
    Production healthcheck verifying classifier readiness and artifact status.
    """
    clf = classifier()
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        model_loaded=clf.model is not None,
        model_accuracy=clf.accuracy,
        classes=clf.classes
    )
