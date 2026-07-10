from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from models.schemas import (
    MarketDataOutput,
    HistoricalRegimeOutput,
    TechnicalAnalysisOutput,
    NewsIntelligenceOutput,
    MacroEconomyOutput,
    OptionsFlowOutput,
    RiskManagerOutput,
    MLPredictionOutput,
    PortfolioManagerOutput,
    ExecutionOutput,
    AgentTimelineLog
)


class HedgeFundState(TypedDict, total=False):
    """
    LangGraph state schema representing the institutional data and multi-agent workflow state.
    Each agent reads from this state and injects its typed output and timeline log.
    """
    task_id: str
    ticker: str
    status: str
    error: Optional[str]

    # Agent outputs
    market_data: Optional[MarketDataOutput]
    historical_regime: Optional[HistoricalRegimeOutput]
    technical_analysis: Optional[TechnicalAnalysisOutput]
    news_intelligence: Optional[NewsIntelligenceOutput]
    macro_economy: Optional[MacroEconomyOutput]
    options_flow: Optional[OptionsFlowOutput]
    risk_manager: Optional[RiskManagerOutput]
    ml_prediction: Optional[MLPredictionOutput]
    portfolio_manager: Optional[PortfolioManagerOutput]
    execution_plan: Optional[ExecutionOutput]

    # Timeline execution log (streamed over WebSockets)
    timeline_logs: List[AgentTimelineLog]
