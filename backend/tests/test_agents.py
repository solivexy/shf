import pytest
import asyncio
from models.state import HedgeFundState
from agents.market_data_agent import market_data_agent_node
from agents.technical_analysis_agent import technical_analysis_agent_node
from agents.news_intelligence_agent import news_intelligence_agent_node
from agents.macro_economy_agent import macro_economy_agent_node
from agents.options_flow_agent import options_flow_agent_node
from agents.risk_manager_agent import risk_manager_agent_node
from agents.ml_prediction_agent import ml_prediction_agent_node
from agents.portfolio_manager_agent import portfolio_manager_agent_node
from agents.execution_agent import execution_agent_node
from utils.cache import cache_manager


@pytest.mark.asyncio
async def test_all_agents_pipeline_sequential():
    await cache_manager.connect()
    
    state: HedgeFundState = {
        "task_id": "test_task_001",
        "ticker": "AAPL",
        "status": "RUNNING",
        "timeline_logs": []
    }

    # 1. Market Data Agent
    state = await market_data_agent_node(state)
    assert "market_data" in state
    assert state["market_data"].ticker == "AAPL"
    assert state["market_data"].current_price > 0

    # 2. Technical Analysis Agent
    state = await technical_analysis_agent_node(state)
    assert "technical_analysis" in state
    assert state["technical_analysis"].bullish_score >= 0

    # 3. News Intelligence Agent
    state = await news_intelligence_agent_node(state)
    assert "news_intelligence" in state
    assert state["news_intelligence"].sentiment in ["Bullish", "Neutral", "Bearish"]

    # 4. Macro Economy Agent
    state = await macro_economy_agent_node(state)
    assert "macro_economy" in state
    assert -100.0 <= state["macro_economy"].macro_score <= 100.0

    # 5. Options Flow Agent
    state = await options_flow_agent_node(state)
    assert "options_flow" in state
    assert state["options_flow"].put_call_ratio > 0

    # 6. Risk Manager Agent
    state = await risk_manager_agent_node(state)
    assert "risk_manager" in state
    assert state["risk_manager"].sharpe_ratio != 0

    # 7. ML Prediction Agent
    state = await ml_prediction_agent_node(state)
    assert "ml_prediction" in state
    assert 0.0 <= state["ml_prediction"].probability_up <= 1.0

    # 8. Portfolio Manager Agent
    state = await portfolio_manager_agent_node(state)
    assert "portfolio_manager" in state
    assert state["portfolio_manager"].decision in ["Strong Buy", "Buy", "Hold", "Reduce", "Sell", "Strong Sell"]

    # 9. Execution Agent
    state = await execution_agent_node(state)
    assert "execution_plan" in state
    assert state["execution_plan"].execution_warning == "SIMULATION ONLY - NO REAL MONEY ORDERS PLACED"
    assert len(state["timeline_logs"]) >= 9
