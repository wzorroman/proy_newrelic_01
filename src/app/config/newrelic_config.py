"""
Configuración centralizada para NewRelic
"""
import os
import newrelic.agent
from app.config.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class NewRelicConfig:
    """Clase para manejar la configuración e inicialización de NewRelic"""

    @staticmethod
    def setup_environment():
        """Configurar variables de entorno para NewRelic"""
        # Establecer variables de entorno explícitamente
        env_vars = {
            'NEW_RELIC_LICENSE_KEY': settings.new_relic_license_key or '',
            'NEW_RELIC_APP_NAME': settings.new_relic_app_name,
            'NEW_RELIC_LOG': 'stdout',
            'NEW_RELIC_LOG_LEVEL': 'info',
            'NEW_RELIC_MONITOR_MODE': 'true',
            'NEW_RELIC_DISTRIBUTED_TRACING_ENABLED': 'true',
        }

        for key, value in env_vars.items():
            if not os.getenv(key):  # Solo establecer si no existe
                os.environ[key] = value
                logger.debug(f"Set environment variable: {key}")

        return env_vars

    @staticmethod
    def is_license_valid():
        """Verificar si la license key es válida"""
        if not settings.new_relic_license_key:
            return False
        if settings.new_relic_license_key == 'your_license_key_here':
            return False
        if len(settings.new_relic_license_key) < 10:  # Validación básica
            return False
        return True

    @staticmethod
    def is_newrelic_already_initialized():
        """Verificar si NewRelic ya fue inicializado por el entrypoint"""
        # Verificar si estamos corriendo bajo newrelic-admin run-program
        import sys
        if 'newrelic' in sys.modules:
            try:
                # Intentar acceder a la configuración global
                config = newrelic.agent.global_settings()
                return config is not None
            except:
                return False
        return False

    @staticmethod
    def initialize_newrelic():
        """Inicializar NewRelic solo si no está ya inicializado"""
        # Configurar entorno primero
        NewRelicConfig.setup_environment()

        # Verificar si NewRelic ya está inicializado por el entrypoint
        if NewRelicConfig.is_newrelic_already_initialized():
            logger.info("✅ NewRelic already initialized by entrypoint")
            return True

        # Verificar license key
        if not NewRelicConfig.is_license_valid():
            logger.warning("⚠️ NewRelic license key not configured or invalid. Running without NewRelic monitoring.")
            return False

        try:
            # Inicializar NewRelic solo si no está ya inicializado
            newrelic.agent.initialize(
                config_file='newrelic.ini',
                environment=settings.fastapi_env
            )

            logger.info(f"✅ NewRelic initialized successfully for app: {settings.new_relic_app_name}")
            logger.info(f"✅ NewRelic environment: {settings.fastapi_env}")

            return True

        except Exception as e:
            logger.error(f"❌ NewRelic initialization failed: {e}")
            return False

    @staticmethod
    def get_config_status():
        """Obtener estado de la configuración de NewRelic"""
        return {
            'license_configured': NewRelicConfig.is_license_valid(),
            'app_name': settings.new_relic_app_name,
            'environment': settings.fastapi_env,
            'initialized_by_entrypoint': NewRelicConfig.is_newrelic_already_initialized(),
            'license_key_preview': f"{settings.new_relic_license_key[:8]}...{settings.new_relic_license_key[-8:]}" if settings.new_relic_license_key and NewRelicConfig.is_license_valid() else 'Not configured'
        }

# Inicializar NewRelic al importar el módulo - PERO solo si no está ya inicializado
NEWRELIC_ENABLED = NewRelicConfig.initialize_newrelic()
