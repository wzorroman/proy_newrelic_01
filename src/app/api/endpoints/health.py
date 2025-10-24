import time
from fastapi import APIRouter, Depends
from app.models.schemas import HealthResponse
from app.utils.newrelic_monitor import NewRelicMonitor
from app.dependencies.dependencies import get_common_parameters

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Endpoint para verificar el estado del servicio",
    tags=["health"]
)
async def health_check(common_params: dict = Depends(get_common_parameters)):
    """Health check endpoint"""
    # Record health check metric
    NewRelicMonitor.record_custom_metric('Custom/HealthCheck', 1)
    NewRelicMonitor.add_custom_attribute('endpoint', 'health_check')
    NewRelicMonitor.add_custom_attribute('health_status', 'healthy')

    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        service="fastapi-newrelic-demo"
    )
