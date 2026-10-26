from fastapi import APIRouter
from app.api.endpoints import analyze, history, stats, health

api_router = APIRouter()

# Include feature routers
api_router.include_router(analyze.router)
api_router.include_router(history.router)
api_router.include_router(stats.router)
api_router.include_router(health.router)
