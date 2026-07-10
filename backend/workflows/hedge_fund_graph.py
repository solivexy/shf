import logging
from typing import Callable, Coroutine, Optional, Any
from langgraph.graph import StateGraph, START, END
from models.state import HedgeFundState

from agents.market_data_agent import market_data_agent_node
from agents.historical_regime_agent import historical_regime_agent_node
from agents.technical_analysis_agent import technical_analysis_agent_node
from agents.news_intelligence_agent import news_intelligence_agent_node
from agents.macro_economy_agent import macro_economy_agent_node
from agents.options_flow_agent import options_flow_agent_node
from agents.risk_manager_agent import risk_manager_agent_node
from agents.ml_prediction_agent import ml_prediction_agent_node
from agents.portfolio_manager_agent import portfolio_manager_agent_node
from agents.execution_agent import execution_agent_node

logger = logging.getLogger("hedge_fund_graph")


def build_hedge_fund_graph(
    step_callback: Optional[Callable[[HedgeFundState, str], Coroutine[Any, Any, None]]] = None
) -> StateGraph:
    """
    Constructs and compiles the LangGraph multi-agent workflow StateGraph.
    Connects: Market Data -> Historical Regime -> Technical -> News -> Macro -> Options -> Risk -> ML -> Portfolio Manager -> Execution.
    Supports optional async step_callback for real-time WebSocket event broadcasting.
    """
    def make_wrapped_node(node_fn, name: str):
        async def wrapper(state: HedgeFundState) -> HedgeFundState:
            logger.info(f"Executing Graph Node: {name}")
            try:
                state = await node_fn(state)
                if step_callback:
                    await step_callback(state, name)
                return state
            except Exception as e:
                logger.error(f"Error executing graph node {name}: {e}")
                state["error"] = f"Node {name} failed: {str(e)}"
                if step_callback:
                    await step_callback(state, name)
                return state
        return wrapper

    # For compilation, langgraph requires standard async nodes
    workflow = StateGraph(HedgeFundState)

    workflow.add_node("market_data", make_wrapped_node(market_data_agent_node, "market_data") if step_callback else market_data_agent_node)
    workflow.add_node("historical_regime", make_wrapped_node(historical_regime_agent_node, "historical_regime") if step_callback else historical_regime_agent_node)
    workflow.add_node("technical_analysis", make_wrapped_node(technical_analysis_agent_node, "technical_analysis") if step_callback else technical_analysis_agent_node)
    workflow.add_node("news_intelligence", make_wrapped_node(news_intelligence_agent_node, "news_intelligence") if step_callback else news_intelligence_agent_node)
    workflow.add_node("macro_economy", make_wrapped_node(macro_economy_agent_node, "macro_economy") if step_callback else macro_economy_agent_node)
    workflow.add_node("options_flow", make_wrapped_node(options_flow_agent_node, "options_flow") if step_callback else options_flow_agent_node)
    workflow.add_node("risk_manager", make_wrapped_node(risk_manager_agent_node, "risk_manager") if step_callback else risk_manager_agent_node)
    workflow.add_node("ml_prediction", make_wrapped_node(ml_prediction_agent_node, "ml_prediction") if step_callback else ml_prediction_agent_node)
    workflow.add_node("portfolio_manager", make_wrapped_node(portfolio_manager_agent_node, "portfolio_manager") if step_callback else portfolio_manager_agent_node)
    workflow.add_node("execution", make_wrapped_node(execution_agent_node, "execution") if step_callback else execution_agent_node)

    # Define strict institutional execution flow
    workflow.add_edge(START, "market_data")
    workflow.add_edge("market_data", "historical_regime")
    workflow.add_edge("historical_regime", "technical_analysis")
    workflow.add_edge("technical_analysis", "news_intelligence")
    workflow.add_edge("news_intelligence", "macro_economy")
    workflow.add_edge("macro_economy", "options_flow")
    workflow.add_edge("options_flow", "risk_manager")
    workflow.add_edge("risk_manager", "ml_prediction")
    workflow.add_edge("ml_prediction", "portfolio_manager")
    workflow.add_edge("portfolio_manager", "execution")
    workflow.add_edge("execution", END)

    return workflow.compile()


compiled_graph = build_hedge_fund_graph()
