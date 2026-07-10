import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter
from services.backtest_service import backtest_service

logger = logging.getLogger("api_backtest")
router = APIRouter(prefix="/backtest", tags=["Backtest"])


class BacktestRequest(BaseModel):
    ticker: str = "AAPL"
    initial_capital: float = 100_000.0
    strategy_type: Optional[str] = "Multi-Agent Confluence"


@router.post("")
async def run_backtest_endpoint(request: BacktestRequest) -> Dict[str, Any]:
    """
    Runs historical backtest across OHLCV bars using vectorized calculations and returns equity curves and metrics.
    """
    result = await backtest_service.run_backtest(
        ticker=request.ticker,
        initial_capital=request.initial_capital,
        strategy_type=request.strategy_type or "Multi-Agent Confluence"
    )
    return result
