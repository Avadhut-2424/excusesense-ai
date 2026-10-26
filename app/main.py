"""
ExcuseSense AI - Production FastAPI Server
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db
from app.ml.engine import classifier
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables and pre-warm ML classifier
    init_db()
    classifier()
    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Leave Application Classifier & Explainable AI Engine",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount both versioned and root endpoints for complete backward and forward compatibility
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(api_router, prefix="")

@app.get("/", tags=["Root"])
def root_status():
    clf = classifier()
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model_accuracy": clf.accuracy,
        "api_documentation": "/docs",
        "supported_classes": clf.classes,
    }
