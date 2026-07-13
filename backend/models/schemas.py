from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MarketDataOutput(BaseModel):
    ticker: str
    company_name: str = ""
    current_price: float = 0.0
    daily_change_percent: float = 0.0
    volume: int = 0
    market_cap: float = 0.0
    float_shares: float = 0.0
    shares_outstanding: float = 0.0
    sector: str = "Unknown"
    industry: str = "Unknown"
    earnings_calendar: List[Dict[str, Any]] = Field(default_factory=list)
    dividend_history: List[Dict[str, Any]] = Field(default_factory=list)
    ohlcv_summary: Dict[str, Any] = Field(default_factory=dict)
    ohlcv_bars: List[Dict[str, Any]] = Field(default_factory=list)
    source_used: str = "yfinance"


class TechnicalAnalysisOutput(BaseModel):
    ticker: str
    bullish_score: float = 50.0
    bearish_score: float = 50.0
    neutral_score: float = 50.0
    trend_status: str = "Neutral / Consolidation"
    indicators: Dict[str, Any] = Field(default_factory=dict)
    detected_patterns: List[str] = Field(default_factory=list)


class NewsIntelligenceOutput(BaseModel):
    ticker: str
    sentiment: str = "Neutral"  # Bullish, Neutral, Bearish
    score: float = 0.0          # -100 to +100
    confidence: float = 70.0    # 0 to 100
    summary: str = ""
    catalysts: List[Dict[str, Any]] = Field(default_factory=list)
    headlines: List[Dict[str, Any]] = Field(default_factory=list)
    articles_analyzed: int = 0


class HistoricalRegimeOutput(BaseModel):
    ticker: str
    cagr_5y: float = 0.0
    cagr_3y: float = 0.0
    cagr_1y: float = 0.0
    sharpe_ratio_5y: float = 0.0
    sortino_ratio_5y: float = 0.0
    max_drawdown_percent: float = 0.0
    volatility_regime: str = "Normal / Consolidation"
    cyclicality_verdict: str = "Secular Growth / Structural Expansion"
    tail_risk_var_95: float = -2.4
    monthly_seasonality: List[Dict[str, Any]] = Field(default_factory=list)
    regime_summary: str = ""
    bars_analyzed: int = 1260


class MacroEconomyOutput(BaseModel):
    macro_score: float = 0.0    # -100 to +100
    risk_score: float = 50.0    # 0 to 100
    economic_outlook: str = ""
    indicators: Dict[str, Any] = Field(default_factory=dict)


class OptionsFlowOutput(BaseModel):
    ticker: str
    institutional_sentiment: str = "Neutral/Theta Skew"
    confidence: float = 70.0
    risk_level: str = "Medium"  # Low, Medium, High, Extreme
    put_call_ratio: float = 1.0
    max_pain_strike: float = 0.0
    iv_rank: float = 50.0
    iv_percentile: float = 50.0
    gamma_exposure_skew: str = "Balanced"
    unusual_activity_summary: str = ""


class RiskManagerOutput(BaseModel):
    ticker: str
    max_drawdown_percent: float = 0.0
    sharpe_ratio: float = 1.0
    sortino_ratio: float = 1.2
    beta: float = 1.0
    correlation_spy: float = 0.75
    annualized_volatility: float = 25.0
    var_95_percent: float = -2.5
    expected_shortfall_percent: float = -3.8
    liquidity_risk_score: str = "Low"
    recommended_stop_loss: float = 0.0
    recommended_take_profit: float = 0.0
    max_position_size_limit: str = "5% of Portfolio"
    risk_category: str = "Medium"  # Low, Medium, High, Extreme


class MLPredictionOutput(BaseModel):
    ticker: str
    probability_up: float = 0.50
    expected_return_percent: float = 0.0
    predicted_direction: str = "SIDEWAYS"  # UP, DOWN, SIDEWAYS
    feature_importance: Dict[str, float] = Field(default_factory=dict)
    model_used: str = "Ensemble (XGBoost + LightGBM + Random Forest)"


class PortfolioManagerOutput(BaseModel):
    ticker: str
    decision_owned: str = "Hold"  # Hold, Reduce, Sell, Strong Sell
    decision_not_owned: str = "Wait"  # Strong Buy, Buy, Wait / Do Not Buy
    confidence: float = 50.0
    position_size: str = "0%"
    risk: str = "Medium"
    investment_horizon: str = "Dynamic"
    bullish_reasons: List[str] = Field(default_factory=list)
    bearish_reasons: List[str] = Field(default_factory=list)
    summary: str = ""
    mandate_summary: Optional[str] = None


class ExecutionOutput(BaseModel):
    ticker: str
    entry_price: float = 0.0
    ideal_buy_zone: str = "$0.00 - $0.00"
    stop_loss: str = "$0.00 (0.0%)"
    take_profit: str = "$0.00 (+0.0%)"
    risk_reward_ratio: str = "1 : 2.0"
    suggested_order_type: str = "Limit Order on Pullback"
    trade_checklist: List[Dict[str, Any]] = Field(default_factory=list)
    execution_warning: str = "INSTITUTIONAL CLIENT ORDER PROTOCOL: ROUTE VIA ICEBERG / TWAP ALGORITHM TO MINIMIZE MARKET IMPACT."


class AgentTimelineLog(BaseModel):
    agent_name: str
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
    runtime_ms: float = 0.0
    confidence: Optional[float] = None
    summary: Optional[str] = None
    reasoning: Optional[str] = None
    output_json: Optional[Dict[str, Any]] = None


class AnalysisRunResult(BaseModel):
    task_id: str
    ticker: str
    status: str = "COMPLETED"  # RUNNING, COMPLETED, FAILED
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timeline_logs: List[AgentTimelineLog] = Field(default_factory=list)
    market_data: Optional[MarketDataOutput] = None
    historical_regime: Optional[HistoricalRegimeOutput] = None
    technical_analysis: Optional[TechnicalAnalysisOutput] = None
    news_intelligence: Optional[NewsIntelligenceOutput] = None
    macro_economy: Optional[MacroEconomyOutput] = None
    options_flow: Optional[OptionsFlowOutput] = None
    risk_manager: Optional[RiskManagerOutput] = None
    ml_prediction: Optional[MLPredictionOutput] = None
    portfolio_manager: Optional[PortfolioManagerOutput] = None
    execution_plan: Optional[ExecutionOutput] = None


class AnalyzeRequest(BaseModel):
    ticker: str
    options: Optional[Dict[str, Any]] = None


class BatchAnalyzeRequest(BaseModel):
    tickers: List[str]
    options: Optional[Dict[str, Any]] = None
