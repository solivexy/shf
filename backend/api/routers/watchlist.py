import logging
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from database.mongodb import mongodb_manager
from services.analysis_service import analysis_service

logger = logging.getLogger("api_watchlist")
router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


class WatchlistUpdateRequest(BaseModel):
    tickers: List[str]
    name: str = "default"


@router.get("/{name}", response_model=List[str])
async def get_watchlist(name: str = "default"):
    """
    Get all ticker symbols in the specified watchlist.
    """
    return await mongodb_manager.get_watchlist(name)


@router.post("/update")
async def update_watchlist(request: WatchlistUpdateRequest):
    """
    Update the list of tickers in a watchlist.
    """
    await mongodb_manager.update_watchlist(request.tickers, request.name)
    return {"status": "success", "name": request.name, "tickers": request.tickers}


@router.post("/scan/{name}")
async def trigger_watchlist_scan(name: str = "default"):
    """
    Immediately triggers parallel multi-agent analysis runs for every ticker in the watchlist.
    """
    tickers = await mongodb_manager.get_watchlist(name)
    tasks = []
    for t in tickers:
        res = await analysis_service.start_analysis_job(t)
        tasks.append({"ticker": t, "task_id": res.task_id})
    return {"status": "scan_triggered", "name": name, "tasks": tasks}
