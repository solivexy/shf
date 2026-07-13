import pytest
import asyncio
from workflows.hedge_fund_graph import build_hedge_fund_graph
from models.state import HedgeFundState
from utils.cache import cache_manager


@pytest.mark.asyncio
async def test_compiled_langgraph_execution():
    await cache_manager.connect()
    
    steps_hit = []
    async def step_cb(state: HedgeFundState, name: str):
        steps_hit.append(name)

    graph = build_hedge_fund_graph(step_callback=step_cb)
    initial_state: HedgeFundState = {
        "task_id": "graph_test_001",
        "ticker": "NVDA",
        "status": "RUNNING",
        "timeline_logs": []
    }

    final_state = await graph.ainvoke(initial_state)
    assert final_state.get("error") is None
    assert "market_data" in final_state
    assert "portfolio_manager" in final_state
    assert "execution_plan" in final_state
    assert len(steps_hit) >= 9
    assert steps_hit[0] == "market_data"
    assert steps_hit[-1] == "execution"
