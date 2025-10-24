import newrelic.agent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Variable global para controlar si NewRelic está activo
NEWRELIC_ENABLED = False

def set_newrelic_status(enabled: bool):
    """Establecer el estado de NewRelic"""
    global NEWRELIC_ENABLED
    NEWRELIC_ENABLED = enabled
    logger.info(f"NewRelic monitor status set to: {'ENABLED' if enabled else 'DISABLED'}")

class NewRelicMonitor:
    """Wrapper para monitoreo con NewRelic usando API actual"""

    @staticmethod
    def record_custom_metric(name: str, value: float):
        """Registrar métrica personalizada"""
        if not NEWRELIC_ENABLED:
            return

        try:
            newrelic.agent.record_custom_metric(name, value)
            logger.debug(f"Metric recorded: {name} = {value}")
        except Exception as e:
            logger.warning(f"Failed to record metric {name}: {e}")

    @staticmethod
    def record_custom_event(event_type: str, params: dict):
        """Registrar evento personalizado"""
        if not NEWRELIC_ENABLED:
            return

        try:
            newrelic.agent.record_custom_event(event_type, params)
            logger.debug(f"Event recorded: {event_type}")
        except Exception as e:
            logger.warning(f"Failed to record event {event_type}: {e}")

    @staticmethod
    def notice_error(exception: Exception, params: dict = None):
        """Registrar error en NewRelic"""
        if not NEWRELIC_ENABLED:
            return

        try:
            # Para la versión actual de NewRelic
            if params:
                # Agregar atributos al error
                transaction = newrelic.agent.current_transaction()
                if transaction:
                    for key, value in params.items():
                        transaction.add_custom_attribute(key, value)

            newrelic.agent.notice_error(exception)
            logger.debug(f"Error recorded: {type(exception).__name__}")
        except Exception as e:
            logger.warning(f"Failed to record error: {e}")

    @staticmethod
    def add_custom_attribute(key: str, value: str):
        """Agregar atributo personalizado a la transacción actual"""
        if not NEWRELIC_ENABLED:
            return

        try:
            transaction = newrelic.agent.current_transaction()
            if transaction:
                transaction.add_custom_attribute(key, value)
                logger.debug(f"Attribute added: {key} = {value}")
            else:
                logger.debug("No active transaction for attribute")
        except Exception as e:
            logger.warning(f"Failed to add attribute {key}: {e}")

    @staticmethod
    def set_transaction_name(name: str):
        """Establecer nombre personalizado para la transacción"""
        if not NEWRELIC_ENABLED:
            return

        try:
            transaction = newrelic.agent.current_transaction()
            if transaction:
                transaction.name = name
                logger.debug(f"Transaction name set: {name}")
        except Exception as e:
            logger.warning(f"Failed to set transaction name: {e}")
