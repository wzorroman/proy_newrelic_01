#!/usr/bin/env python3
"""
Main entry point for the FastAPI NewRelic Demo Application
"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Importar configuración centralizada
from app.config.config import settings
from app.config.newrelic_config import NEWRELIC_ENABLED
from app.models.database import init_db
from app.api.endpoints import health, data, users, slow_operation
from app.utils.logger import setup_logger
from app.utils.newrelic_monitor import NewRelicMonitor, set_newrelic_status

logger = setup_logger(__name__)

# Configurar estado de NewRelic
set_newrelic_status(NEWRELIC_ENABLED)

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    logger.info(f"🚀 Application started in {settings.fastapi_env} mode")

    # Mostrar estado de NewRelic
    from app.config.newrelic_config import NewRelicConfig
    status = NewRelicConfig.get_config_status()

    if NEWRELIC_ENABLED:
        if status['initialized_by_entrypoint']:
            logger.info("✅ NewRelic monitoring is ACTIVE (initialized by entrypoint)")
        else:
            logger.info("✅ NewRelic monitoring is ACTIVE (initialized by application)")
        logger.info(f"📊 NewRelic Config: App='{status['app_name']}', Env='{status['environment']}'")
    else:
        logger.info("⚠️ NewRelic monitoring is INACTIVE")

    yield

    # Shutdown
    logger.info("🛑 Application shutting down")

# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description="Una API de demostración con FastAPI y NewRelic integrado",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router,
    prefix=settings.api_v1_prefix,
    tags=["health"]
)
app.include_router(
    data.router,
    prefix=settings.api_v1_prefix,
    tags=["data"]
)
app.include_router(
    users.router,
    prefix=settings.api_v1_prefix,
    tags=["users"]
)
app.include_router(
    slow_operation.router,
    prefix=settings.api_v1_prefix,
    tags=["monitoring"]
)

@app.middleware("http")
async def newrelic_middleware(request: Request, call_next):
    """Middleware para monitoreo de NewRelic"""
    start_time = time.time()

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Solo registrar métricas si NewRelic está activo
        if NEWRELIC_ENABLED:
            NewRelicMonitor.record_custom_metric('Custom/RequestCount', 1)
            NewRelicMonitor.record_custom_metric('Custom/ResponseTime', process_time)
            NewRelicMonitor.add_custom_attribute('response_status', str(response.status_code))
            NewRelicMonitor.add_custom_attribute('request_path', request.url.path)
            NewRelicMonitor.add_custom_attribute('request_method', request.method)

        logger.debug(f"Request processed: {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} - Error: {e}")

        # Registrar error solo si NewRelic está activo
        if NEWRELIC_ENABLED:
            NewRelicMonitor.notice_error(e, {
                'request_path': request.url.path,
                'request_method': request.method,
                'processing_time': str(process_time)
            })
            NewRelicMonitor.record_custom_metric('Custom/RequestError', 1)

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint"""
    from app.config.newrelic_config import NewRelicConfig
    status = NewRelicConfig.get_config_status()

    newrelic_status = "active" if NEWRELIC_ENABLED else "inactive"
    return {
        "message": "FastAPI NewRelic Demo API",
        "status": "running",
        "version": settings.project_version,
        "documentation": "/docs",
        "environment": settings.fastapi_env,
        "newrelic_status": newrelic_status,
        "newrelic_app_name": status['app_name'],
        "newrelic_license_configured": status['license_configured'],
        "newrelic_initialized_by": "entrypoint" if status['initialized_by_entrypoint'] else "application"
    }

@app.get("/health", include_in_schema=False)
async def health_check():
    """Simple health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.fastapi_debug,
        log_level="info"
    )
