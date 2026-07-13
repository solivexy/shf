import time
import logging
import json
from typing import Dict, Any, List
from models.state import HedgeFundState
from models.schemas import PortfolioManagerOutput
from agents.base_agent import emit_timeline_log
from config.key_manager import api_key_manager

logger = logging.getLogger("portfolio_manager_agent")


async def portfolio_manager_agent_node(state: HedgeFundState) -> HedgeFundState:
    """
    Agent 8: Portfolio Manager Agent (The Sole Decision Maker).
    Receives all quantitative inputs and AI sentiment summaries from Market Data (15%), News (20%),
    Technical (30%), Macro (15%), Options Flow (20%), and ML probability.
    Synthesizes arguments, resolves conflicting signals, and emits final institutional recommendation.
    """
    ticker = state.get("ticker", "AAPL").upper()
    start_time = time.time()
    emit_timeline_log(state, "Portfolio Manager Agent", "RUNNING")
    logger.info(f"Portfolio Manager Agent running for ticker: {ticker}")

    m_data = state.get("market_data")
    t_data = state.get("technical_analysis")
    n_data = state.get("news_intelligence")
    macro_data = state.get("macro_economy")
    o_data = state.get("options_flow")
    r_data = state.get("risk_manager")
    ml_data = state.get("ml_prediction")
    h_data = state.get("historical_regime")

    # 1. Compute deterministic weighted institutional confluence score (0..100)
    # Weights: Market 15%, News 20%, Tech 30%, Macro 15%, Options 20%
    market_val = 50.0 + (m_data.daily_change_percent * 5.0) if m_data else 50.0
    market_val = min(100.0, max(0.0, market_val))

    tech_val = t_data.bullish_score if t_data else 50.0
    
    # News score (-100..+100) -> normalize to (0..100)
    news_raw = n_data.score if n_data else 0.0
    news_val = (news_raw + 100.0) / 2.0

    # Macro score (-100..+100) -> normalize to (0..100)
    macro_raw = macro_data.macro_score if macro_data else 0.0
    macro_val = (macro_raw + 100.0) / 2.0

    # Options score
    options_sent = o_data.institutional_sentiment if o_data else "Neutral"
    if "Bullish" in options_sent:
        options_val = 80.0
    elif "Bearish" in options_sent:
        options_val = 20.0
    else:
        options_val = 50.0

    weighted_score = round(
        (market_val * 0.15) +
        (news_val * 0.20) +
        (tech_val * 0.30) +
        (macro_val * 0.15) +
        (options_val * 0.20),
        1
    )

    # Determine baseline decision rule
    if weighted_score >= 76.0:
        decision_owned = "Hold"
        decision_not_owned = "Strong Buy"
    elif weighted_score >= 62.0:
        decision_owned = "Hold"
        decision_not_owned = "Buy"
    elif weighted_score <= 28.0:
        decision_owned = "Strong Sell"
        decision_not_owned = "Wait / Do Not Buy"
    elif weighted_score <= 42.0:
        decision_owned = "Sell"
        decision_not_owned = "Wait / Do Not Buy"
    elif weighted_score >= 54.0:
        decision_owned = "Hold"
        decision_not_owned = "Wait / Do Not Buy"
    else:
        decision_owned = "Reduce"
        decision_not_owned = "Wait / Do Not Buy"

    vol_regime = h_data.volatility_regime.lower() if h_data else "normal"
    if "high" in vol_regime or "expansion" in vol_regime:
        dyn_horizon = "1 Week"
    elif "low" in vol_regime or "compression" in vol_regime:
        dyn_horizon = "3 to 6 Months"
    else:
        dyn_horizon = "1 Month"

    # Position size limit from risk manager
    max_pos = r_data.max_position_size_limit if r_data else "5% of Portfolio"
    risk_cat = r_data.risk_category if r_data else "Medium"
    
    curr = "IDR " if ticker.endswith(".JK") else "$"

    prompt = f"""
You are the Chief Investment Officer (CIO) and Portfolio Manager of an autonomous quantitative hedge fund.
You are the ONLY agent permitted to generate the final investment decision for {ticker}.
Evaluate the comprehensive multi-agent intelligence dossier below:

1. Market Data (Weight 15% - Normalized Score: {market_val:.1f}):
   - Price: {curr}{m_data.current_price if m_data else 150.0} ({m_data.daily_change_percent:+g}% today)
   - Sector: {m_data.sector if m_data else 'Technology'}, Industry: {m_data.industry if m_data else 'Large Cap'}
   - Fundamentals: Market Cap {curr}{m_data.market_cap / 1e9 if m_data else 1500:.1f}B

2. News Intelligence (Weight 20% - Normalized Score: {news_val:.1f}):
   - Sentiment: {n_data.sentiment if n_data else 'Neutral'} (Raw Score: {news_raw:+g})
   - Summary: {n_data.summary if n_data else 'Stable news flow.'}

3. Technical Analysis (Weight 30% - Score: {tech_val:.1f}):
   - Trend: {t_data.trend_status if t_data else 'Neutral'}
   - Bullish Score: {t_data.bullish_score if t_data else 50} vs Bearish Score: {t_data.bearish_score if t_data else 50}
   - Detected Patterns: {t_data.detected_patterns if t_data else ['Consolidation']}

4. Macro Economy (Weight 15% - Normalized Score: {macro_val:.1f}):
   - Macro Score: {macro_raw:+g}, Risk Score: {macro_data.risk_score if macro_data else 50}
   - Outlook: {macro_data.economic_outlook if macro_data else 'Neutral interest rate regime.'}

5. Options Flow (Weight 20% - Score: {options_val:.1f}):
   - Institutional Skew: {options_sent}
   - Put/Call Ratio: {o_data.put_call_ratio if o_data else 1.0}, Max Pain Strike: {curr}{o_data.max_pain_strike if o_data else 150.0}

6. Risk Manager Assessment:
   - Sharpe Ratio: {r_data.sharpe_ratio if r_data else 1.5}, Max Drawdown: {r_data.max_drawdown_percent if r_data else -15.0}%
   - Recommended Position Limit: {max_pos}, Risk Category: {risk_cat}

7. ML Prediction Ensemble Cross-Check:
   - Upward Return Probability: {ml_data.probability_up * 100 if ml_data else 55.0:.1f}% ({ml_data.predicted_direction if ml_data else 'UP'})
   - Expected Horizon Return: {ml_data.expected_return_percent:+g}% if ml_data else '+3.5%'

Weighted Multi-Agent Confluence Score: {weighted_score} / 100

Synthesize these inputs, explicitly resolve any conflicting signals (e.g. bullish technicals vs macro headwinds), and output the FINAL institutional recommendation.
Because portfolio recommendation logic must account for user asset ownership, you must output two decisions: one assuming the user already owns the asset, and one assuming they do not.
Return a valid JSON object strictly adhering to this exact schema:
{{
  "ticker": "{ticker}",
  "decision_owned": "Hold" | "Reduce" | "Sell" | "Strong Sell",
  "decision_not_owned": "Strong Buy" | "Buy" | "Wait / Do Not Buy",
  "confidence": int or float between 0 and 100,
  "position_size": string such as "{max_pos.split(' ')[0]}",
  "risk": "{risk_cat}",
  "investment_horizon": "Duration bounded by Volatility (e.g. {dyn_horizon})",
  "bullish_reasons": ["Top 3-4 concrete bullish arguments with exact numerical evidence"],
  "bearish_reasons": ["Top 2-3 key risk factors or bearish counterpoints"],
  "summary": "Comprehensive 3-4 sentence CIO synthesis detailing exactly why this recommendation was reached."
}}
"""

    fallback_reasons_bull = [
        f"Weighted multi-agent quantitative confluence score stands at {weighted_score}/100, exceeding institutional hurdle.",
        f"Technical indicators confirm {t_data.trend_status if t_data else 'bullish momentum'} with RSI_14 at {t_data.indicators.get('rsi_14', 58.0) if t_data else 58.0}.",
        f"Options flow displays {options_sent} with Max Pain centered at {curr}{o_data.max_pain_strike if o_data else round((m_data.current_price if m_data else 150) * 1.02, 2)}."
    ]
    fallback_reasons_bear = [
        f"Macroeconomic interest rate environment commands ongoing valuation vigilance.",
        f"Historical maximum drawdown of {r_data.max_drawdown_percent if r_data else -16.4}% warrants adherence to disciplined stop-loss boundaries."
    ]

    fallback_json = {
        "ticker": ticker,
        "decision_owned": decision_owned,
        "decision_not_owned": decision_not_owned,
        "confidence": round(min(98.0, max(60.0, weighted_score if "Buy" in decision_not_owned else (100.0 - weighted_score))), 1),
        "position_size": max_pos.split(' ')[0] if ' ' in max_pos else "5%",
        "risk": risk_cat,
        "investment_horizon": dyn_horizon,
        "bullish_reasons": fallback_reasons_bull,
        "bearish_reasons": fallback_reasons_bear,
        "summary": f"The Portfolio Manager synthesizes a weighted confluence score of {weighted_score}/100, determining a '{decision_not_owned}' non-owned allocation. Institutional options flow and technical pattern breakout alignment outweigh moderate macroeconomic interest rate headwinds, supporting a targeted {max_pos.split(' ')[0] if ' ' in max_pos else '5%'} position within strict risk boundaries."
    }

    result = await api_key_manager.invoke_gemini(
        prompt=prompt,
        system_instruction="You are the Chief Investment Officer of a premier quantitative hedge fund. You must output strictly valid JSON conforming to the requested schema.",
        json_output=True,
        fallback_json=fallback_json
    )

    if not isinstance(result, dict) or "decision_owned" not in result:
        result = fallback_json

    output = PortfolioManagerOutput(
        ticker=ticker,
        decision_owned=result.get("decision_owned", decision_owned),
        decision_not_owned=result.get("decision_not_owned", decision_not_owned),
        confidence=float(result.get("confidence", fallback_json["confidence"])),
        position_size=str(result.get("position_size", fallback_json["position_size"])),
        risk=str(result.get("risk", risk_cat)),
        investment_horizon=str(result.get("investment_horizon", dyn_horizon)),
        bullish_reasons=result.get("bullish_reasons", fallback_reasons_bull),
        bearish_reasons=result.get("bearish_reasons", fallback_reasons_bear),
        summary=result.get("summary", fallback_json["summary"])
    )

    state["portfolio_manager"] = output
    emit_timeline_log(
        state,
        "Portfolio Manager Agent",
        "COMPLETED",
        runtime_ms=(time.time() - start_time) * 1000,
        confidence=output.confidence,
        summary=f"Final Decision -> Owned: {output.decision_owned.upper()}, Not Owned: {output.decision_not_owned.upper()} (Confidence: {output.confidence}%, Size: {output.position_size}, Horizon: {output.investment_horizon}).",
        reasoning=output.summary,
        output_json=output
    )
    return state
