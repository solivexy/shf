import asyncio
import logging
from celery_app import celery_app
from services.analysis_service import analysis_service
from database.mongodb import mongodb_manager

logger = logging.getLogger("celery_tasks")


@celery_app.task(name="workers.tasks.run_analysis_task")
def run_analysis_task(ticker: str, task_id: str):
    """
    Celery background worker task for running single-ticker multi-agent workflow.
    """
    logger.info(f"Celery worker executing task {task_id} for {ticker}")
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Create task inside running loop or run sync wrapper
        asyncio.run_coroutine_threadsafe(analysis_service.start_analysis_job(ticker, task_id), loop)
    else:
        loop.run_until_complete(analysis_service.start_analysis_job(ticker, task_id))
    return {"status": "started", "task_id": task_id, "ticker": ticker}


@celery_app.task(name="workers.tasks.run_scheduled_watchlist_scan")
def run_scheduled_watchlist_scan():
    """
    Periodic Celery Beat task that automatically runs analysis on all tickers in the default watchlist.
    """
    logger.info("Celery Beat triggered scheduled watchlist scan.")
    async def _scan():
        await mongodb_manager.connect()
        tickers = await mongodb_manager.get_watchlist("default")
        for ticker in tickers:
            await analysis_service.start_analysis_job(ticker)
            await asyncio.sleep(1.0)
    
    try:
        asyncio.run(_scan())
    except Exception as e:
        logger.error(f"Scheduled watchlist scan failed: {e}")
    return {"status": "scan_completed"}
