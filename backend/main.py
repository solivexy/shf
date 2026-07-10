from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from utils.logger import setup_logger
from utils.cache import cache_manager
from database.mongodb import mongodb_manager

from api.routers import analysis, portfolio, watchlist, backtest, reports
from api.websockets import live

settings = get_settings()
logger = setup_logger("main", level=settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await cache_manager.connect()
    await mongodb_manager.connect()
    yield
    # Shutdown
    logger.info("Shutting down Autonomous AI Stock Hedge Fund platform...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Institutional-Grade Multi-Agent AI Stock Hedge Fund Research Platform",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "*"],
    allow_origin_regex="http://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API & WebSocket Routers
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(portfolio.router, prefix="/api/v1")
app.include_router(watchlist.router, prefix="/api/v1")
app.include_router(backtest.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(live.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "redis_connected": cache_manager._redis_available,
        "mongodb_connected": mongodb_manager._mongo_available
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
