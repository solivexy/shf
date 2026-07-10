import time
import logging
import pandas as pd
from models.state import HedgeFundState
from models.schemas import TechnicalAnalysisOutput
from agents.base_agent import emit_timeline_log
from utils.cache import cache_manager
from indicators.technical import calculate_all_indicators, calculate_confluence_scores
from indicators.patterns import detect_classical_patterns

logger = logging.getLogger("technical_analysis_agent")


async def technical_analysis_agent_node(state: HedgeFundState) -> HedgeFundState:
    """
    Agent 2: Technical Analysis Agent.
    100% Deterministic quantitative indicator evaluation and classical chart pattern recognition.
    Strictly forbidden from using LLM approximations for indicator metrics.
    """
    ticker = state.get("ticker", "AAPL").upper()
    start_time = time.time()
    emit_timeline_log(state, "Technical Analysis Agent", "RUNNING")
    logger.info(f"Technical Analysis Agent running for ticker: {ticker}")

    # Load raw DataFrame from cache
    raw_dict = await cache_manager.get(f"df_ohlcv:{ticker}")
    df = None
    if raw_dict:
        try:
            df = pd.DataFrame(raw_dict)
        except Exception as e:
            logger.warning(f"Error reconstructing DataFrame from cache: {e}")

    # Calculate indicators deterministically
    indicators = calculate_all_indicators(df)
    patterns = detect_classical_patterns(df)
    bull_score, bear_score, neut_score = calculate_confluence_scores(indicators)

    # Determine status label based on scores
    if bull_score >= 65.0:
        trend_status = f"Strong Bullish Trend ({bull_score}% Confluence)"
    elif bull_score >= 54.0:
        trend_status = f"Moderate Bullish Bias ({bull_score}% Confluence)"
    elif bear_score >= 65.0:
        trend_status = f"Strong Bearish Breakdown ({bear_score}% Confluence)"
    elif bear_score >= 54.0:
        trend_status = f"Moderate Bearish Pressure ({bear_score}% Confluence)"
    else:
        trend_status = f"Neutral / Consolidation Range ({neut_score}% Neutral)"

    output = TechnicalAnalysisOutput(
        ticker=ticker,
        bullish_score=bull_score,
        bearish_score=bear_score,
        neutral_score=neut_score,
        trend_status=trend_status,
        indicators=indicators,
        detected_patterns=patterns
    )

    state["technical_analysis"] = output
    emit_timeline_log(
        state,
        "Technical Analysis Agent",
        "COMPLETED",
        runtime_ms=(time.time() - start_time) * 1000,
        confidence=round(max(bull_score, bear_score, neut_score), 1),
        summary=f"Computed 11 quantitative indicators & detected: {', '.join(patterns)} ({trend_status}).",
        output_json=output
    )
    return state
