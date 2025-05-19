from fastapi import APIRouter
from app.api import health_metrics, exercises, metadata, quick_log

api_router = APIRouter()

# Add all routers
api_router.include_router(
    metadata.router,
    tags=["metadata"]
)

api_router.include_router(
    health_metrics.router,
    prefix="/health-metrics",
    tags=["health metrics"]
)

api_router.include_router(
    exercises.router,
    prefix="/exercises",
    tags=["exercises"]
)

api_router.include_router(
    quick_log.router,
    prefix="/quick",
    tags=["quick log"]
)
