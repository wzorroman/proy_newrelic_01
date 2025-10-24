import time
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import DataResponse, Metadata
from app.services.api_service import ApiService
from app.utils.logger import setup_logger
from app.utils.newrelic_monitor import NewRelicMonitor
from app.dependencies.dependencies import get_common_parameters

logger = setup_logger(__name__)
router = APIRouter()

@router.get(
    "/data",
    response_model=DataResponse,
    summary="Get Processed Data",
    description="Obtener datos procesados desde una API externa",
    tags=["data"]
)
async def get_data(common_params: dict = Depends(get_common_parameters)):
    """Get processed data from external API"""
    try:
        # Configurar transacción y atributos
        NewRelicMonitor.set_transaction_name("DataProcessing")
        NewRelicMonitor.add_custom_attribute('endpoint', 'get_data')
        NewRelicMonitor.add_custom_attribute('source', 'external_api')

        # Record custom metric
        NewRelicMonitor.record_custom_metric('Custom/DataRequest', 1)

        # Get external data
        external_data = await ApiService.get_external_data()

        # Process data
        processed_data = await ApiService.process_data(external_data)

        # Registrar éxito
        NewRelicMonitor.record_custom_metric('Custom/DataSuccess', 1)
        NewRelicMonitor.add_custom_attribute('data_processed', 'true')
        NewRelicMonitor.add_custom_attribute('data_source', 'jsonplaceholder')

        logger.info("Data processed successfully")

        # CORRECCIÓN: Crear metadata como diccionario en lugar de instancia
        metadata_dict = {
            "processed_at": time.time(),
            "source": "external_api"
        }

        return DataResponse(
            success=True,
            data=processed_data,
            metadata=metadata_dict  # ✅ Pasar como diccionario, no como instancia Metadata
        )

    except Exception as e:
        logger.error(f"Error in get_data: {e}")

        # Registrar error en NewRelic
        NewRelicMonitor.notice_error(e, {
            'endpoint': 'get_data',
            'operation': 'external_api_call',
            'error_type': 'data_processing_error'
        })
        NewRelicMonitor.record_custom_metric('Custom/DataError', 1)
        NewRelicMonitor.add_custom_attribute('data_processed', 'false')

        raise HTTPException(status_code=500, detail="Internal server error")
