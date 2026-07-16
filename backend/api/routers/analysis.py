import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import AnalyzeRequest, BatchAnalyzeRequest, AnalysisRunResult
from services.analysis_service import analysis_service

logger = logging.getLogger("api_analysis")
router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalysisRunResult)
async def analyze_ticker(request: AnalyzeRequest):
    """
    Triggers an autonomous multi-agent analysis run for a single ticker.
    Returns the initial state task_id which can be streamed via WebSocket or checked via GET /status.
    """
    if not request.ticker or len(request.ticker.strip()) == 0:
        raise HTTPException(status_code=400, detail="Ticker symbol cannot be empty.")
    clean_ticker = request.ticker.strip().upper().replace('-', '.')
    result = await analysis_service.start_analysis_job(clean_ticker)
    return result


@router.post("/batch", response_model=List[AnalysisRunResult])
async def analyze_batch(request: BatchAnalyzeRequest):
    """
    Triggers parallel multi-agent analysis runs for multiple tickers simultaneously.
    """
    if not request.tickers or len(request.tickers) == 0:
        raise HTTPException(status_code=400, detail="Must provide at least one ticker symbol.")
    
    results = []
    for t in request.tickers[:10]: # cap at 10 for safety
        clean_t = t.strip().upper().replace('-', '.')
        if clean_t:
            res = await analysis_service.start_analysis_job(clean_t)
            results.append(res)
    return results


@router.get("/status/{task_id}", response_model=AnalysisRunResult)
async def get_analysis_status(task_id: str):
    """
    Retrieves the current execution state and timeline logs of an analysis task.
    """
    res = await analysis_service.get_task_status(task_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Analysis task {task_id} not found.")
    return res


@router.get("/history/{ticker}", response_model=List[Dict[str, Any]])
async def get_ticker_history(ticker: str):
    """
    Retrieves historical analysis runs and CIO recommendations for a ticker.
    """
    clean_ticker = ticker.strip().upper().replace('-', '.')
    history = await analysis_service.get_history(clean_ticker)
    return history
