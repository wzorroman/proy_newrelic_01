from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import SlowOperationResponse
from app.services.api_service import ApiService
from app.utils.logger import setup_logger
from app.utils.newrelic_monitor import NewRelicMonitor
from app.dependencies.dependencies import get_common_parameters

logger = setup_logger(__name__)
router = APIRouter()

@router.get(
    "/slow-operation",
    response_model=SlowOperationResponse,
    summary="Slow Operation",
    description="Simular una operación lenta para monitoreo",
    tags=["monitoring"]
)
async def slow_operation(common_params: dict = Depends(get_common_parameters)):
    """Simulate a slow operation for monitoring"""
    try:
        NewRelicMonitor.set_transaction_name("SlowOperation")
        NewRelicMonitor.add_custom_attribute('endpoint', 'slow_operation')
        NewRelicMonitor.add_custom_attribute('operation_type', 'simulated_processing')

        processing_time = await ApiService.simulate_slow_operation()

        # Record custom metrics
        NewRelicMonitor.record_custom_metric('Custom/SlowOperationTime', processing_time)
        NewRelicMonitor.record_custom_metric('Custom/SlowOperationCount', 1)
        NewRelicMonitor.add_custom_attribute('processing_time_seconds', str(round(processing_time, 3)))

        logger.info(f"Slow operation completed in {processing_time:.3f}s")

        return SlowOperationResponse(
            success=True,
            message="Slow operation completed",
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Error in slow operation: {e}")

        NewRelicMonitor.notice_error(e, {
            'endpoint': 'slow_operation',
            'operation': 'simulated_processing',
            'error_type': 'processing_error'
        })

        raise HTTPException(status_code=500, detail="Internal server error")
