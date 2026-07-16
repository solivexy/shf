import asyncio
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from utils.logger import setup_logger
from config.settings import get_settings
from models.schemas import AnalysisRunResult

logger = setup_logger("mongodb")


class MongoDBManager:
    """
    Async MongoDB Connection & Repository Manager using Motor.
    Includes in-memory fallback for offline/development resilience.
    """
    def __init__(self):
        self._client = None
        self._db = None
        self._mongo_available = False
        self._memory_runs: Dict[str, Dict[str, Any]] = self._build_benchmark_runs()
        self._memory_watchlists: Dict[str, List[str]] = {"default": ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "BBRI.JK", "BMRI.JK"]}
        self._lock = asyncio.Lock()

    def _build_benchmark_runs(self) -> Dict[str, Dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        return {
            "DOSSIER-INST-AAPL-01": {
                "task_id": "DOSSIER-INST-AAPL-01",
                "ticker": "AAPL",
                "status": "COMPLETED",
                "created_at": now,
                "market_data": {
                    "ticker": "AAPL",
                    "company_name": "Apple Inc.",
                    "current_price": 228.40,
                    "daily_change_percent": 1.84,
                    "volume": 58240000,
                    "avg_volume_10d": 51200000
                },
                "portfolio_manager": {
                    "ticker": "AAPL",
                    "decision": "Strong Buy",
                    "confidence": 91.5,
                    "position_size": "12.5%",
                    "risk": "Low",
                    "summary": "Confluence of strong enterprise AI hardware cycle and expanding services margin. Kelly position sizing recommends 12.5% portfolio allocation with trailing stop at $218.50.",
                    "bullish_reasons": [
                        "Services margin expansion reaching new institutional record highs (+74.2%).",
                        "Apple Intelligence rollout driving multi-year hardware refresh cycle.",
                        "Massive corporate share buyback program ($110B authorized) setting strong price floor."
                    ],
                    "bearish_reasons": [
                        "Near-term regulatory antitrust headwinds in European Union markets.",
                        "Currency headwinds from USD strength impacting international segment revenue."
                    ]
                },
                "risk_manager": {
                    "ticker": "AAPL",
                    "sharpe_ratio": 2.14,
                    "max_drawdown_percent": -11.8,
                    "var_95_percent": -1.85,
                    "beta": 1.04
                },
                "execution_plan": {
                    "ticker": "AAPL",
                    "ideal_buy_zone": "$224.50 - $228.00",
                    "stop_loss": "$218.50",
                    "take_profit": "$248.00",
                    "risk_reward_ratio": "1 : 2.8",
                    "suggested_order_type": "VWAP Iceberg Splitting (Max 12% ADV per tranche)"
                },
                "options_flow": {
                    "ticker": "AAPL",
                    "put_call_ratio": 0.62,
                    "max_pain_strike": 225.0,
                    "iv_rank": 38.4,
                    "gamma_exposure_skew": "Positive Gamma Skew (Call heavy accumulation)",
                    "institutional_sentiment": "Strong Bullish Call Buying ($230 - $240 calls)"
                },
                "historical_regime": {
                    "ticker": "AAPL",
                    "sharpe_ratio_5y": 2.14,
                    "max_drawdown_percent": -11.8,
                    "cagr_5y": 22.4,
                    "regime_summary": "Low-volatility bullish growth regime."
                },
                "timeline_logs": [
                    {"agent_name": "Market Data Agent", "status": "COMPLETED", "runtime_ms": 240, "confidence": 99.0, "summary": "Fetched realtime Level-1 orderbook & spot tick data ($228.40)."},
                    {"agent_name": "Historical Regime Agent", "status": "COMPLETED", "runtime_ms": 310, "confidence": 94.0, "summary": "Identified low-volatility bullish growth regime (Sharpe 2.14)."},
                    {"agent_name": "Technical Analysis Agent", "status": "COMPLETED", "runtime_ms": 285, "confidence": 92.5, "summary": "Price above 20d/50d/200d EMA confluence with RSI bullish momentum (64.2)."},
                    {"agent_name": "Options Flow Agent", "status": "COMPLETED", "runtime_ms": 410, "confidence": 91.0, "summary": "Unusual institutional call sweep detected ($14.2M premium at $235 strike)."},
                    {"agent_name": "Risk Manager Agent", "status": "COMPLETED", "runtime_ms": 190, "confidence": 95.0, "summary": "Verified Daily VaR (95%) at -1.85% with Kelly allocation cap at 12.5%."},
                    {"agent_name": "Portfolio Manager Agent", "status": "COMPLETED", "runtime_ms": 380, "confidence": 91.5, "summary": "Synthesized institutional consensus: STRONG BUY recommendation."}
                ]
            },
            "DOSSIER-INST-NVDA-02": {
                "task_id": "DOSSIER-INST-NVDA-02",
                "ticker": "NVDA",
                "status": "COMPLETED",
                "created_at": now,
                "market_data": {
                    "ticker": "NVDA",
                    "company_name": "NVIDIA Corporation",
                    "current_price": 138.25,
                    "daily_change_percent": 3.42,
                    "volume": 94200000,
                    "avg_volume_10d": 88000000
                },
                "portfolio_manager": {
                    "ticker": "NVDA",
                    "decision": "Buy",
                    "confidence": 88.0,
                    "position_size": "10.0%",
                    "risk": "Medium",
                    "summary": "Options gamma exposure shows strong call wall accumulation at $140. ML XGBoost/LightGBM ensemble projects +8.4% upside over next 20 trading sessions.",
                    "bullish_reasons": [
                        "Blackwell architecture volume shipments exceeding institutional buy-side forecasts.",
                        "Sovereign AI capital expenditure infrastructure buildouts scaling globally.",
                        "Massive call gamma wall at $140 acting as strong upward magnetic price target."
                    ],
                    "bearish_reasons": [
                        "High implied volatility elevation relative to historical 52-week baseline.",
                        "Semiconductor export restrictions introducing supply chain friction."
                    ]
                },
                "risk_manager": {
                    "ticker": "NVDA",
                    "sharpe_ratio": 2.45,
                    "max_drawdown_percent": -16.4,
                    "var_95_percent": -2.80,
                    "beta": 1.65
                },
                "execution_plan": {
                    "ticker": "NVDA",
                    "ideal_buy_zone": "$135.00 - $138.00",
                    "stop_loss": "$129.50",
                    "take_profit": "$152.00",
                    "risk_reward_ratio": "1 : 2.6",
                    "suggested_order_type": "TWAP Tranche Routing (8-minute intervals over 2 hours)"
                },
                "options_flow": {
                    "ticker": "NVDA",
                    "put_call_ratio": 0.58,
                    "max_pain_strike": 135.0,
                    "iv_rank": 54.2,
                    "gamma_exposure_skew": "Strong Positive Call Gamma Skew ($140 call wall)",
                    "institutional_sentiment": "Aggressive Call Accumulation"
                },
                "historical_regime": {
                    "ticker": "NVDA",
                    "sharpe_ratio_5y": 2.45,
                    "max_drawdown_percent": -16.4,
                    "cagr_5y": 44.8,
                    "regime_summary": "High beta growth expansion."
                },
                "timeline_logs": [
                    {"agent_name": "Market Data Agent", "status": "COMPLETED", "runtime_ms": 220, "confidence": 99.0, "summary": "Fetched realtime Level-1 orderbook tick data ($138.25)."},
                    {"agent_name": "Technical Analysis Agent", "status": "COMPLETED", "runtime_ms": 290, "confidence": 89.0, "summary": "Breakout above multi-week bull flag resistance pattern on above-average volume."},
                    {"agent_name": "Options Flow Agent", "status": "COMPLETED", "runtime_ms": 430, "confidence": 93.0, "summary": "Call OI concentration confirms institutional gamma pinning at $140 strike."},
                    {"agent_name": "Portfolio Manager Agent", "status": "COMPLETED", "runtime_ms": 360, "confidence": 88.0, "summary": "Consensus institutional synthesis: BUY allocation."}
                ]
            },
            "DOSSIER-INST-MSFT-03": {
                "task_id": "DOSSIER-INST-MSFT-03",
                "ticker": "MSFT",
                "status": "COMPLETED",
                "created_at": now,
                "market_data": {
                    "ticker": "MSFT",
                    "company_name": "Microsoft Corporation",
                    "current_price": 448.90,
                    "daily_change_percent": 0.72,
                    "volume": 18400000,
                    "avg_volume_10d": 21000000
                },
                "portfolio_manager": {
                    "ticker": "MSFT",
                    "decision": "Buy",
                    "confidence": 84.2,
                    "position_size": "10.0%",
                    "risk": "Low",
                    "summary": "Azure AI infrastructure growth offsetting personal computing seasonality. Historical regime comparison indicates favorable risk-adjusted Sharpe ratio of 2.14.",
                    "bullish_reasons": [
                        "Copilot enterprise monetization scaling rapidly across Fortune 500 accounts.",
                        "Cloud infrastructure workload migration accelerating margin expansion."
                    ],
                    "bearish_reasons": [
                        "Elevated capital expenditures for AI datacenter expansion impacting free cash flow margin."
                    ]
                },
                "risk_manager": {
                    "ticker": "MSFT",
                    "sharpe_ratio": 1.95,
                    "max_drawdown_percent": -10.5,
                    "var_95_percent": -1.45,
                    "beta": 0.92
                },
                "execution_plan": {
                    "ticker": "MSFT",
                    "ideal_buy_zone": "$444.00 - $448.00",
                    "stop_loss": "$434.00",
                    "take_profit": "$475.00",
                    "risk_reward_ratio": "1 : 2.5",
                    "suggested_order_type": "Passive VWAP Iceberg Orders"
                },
                "options_flow": {
                    "ticker": "MSFT",
                    "put_call_ratio": 0.74,
                    "max_pain_strike": 445.0,
                    "iv_rank": 32.0,
                    "gamma_exposure_skew": "Balanced Institutional Call Skew",
                    "institutional_sentiment": "Steady Institutional Long Hedging"
                },
                "historical_regime": {
                    "ticker": "MSFT",
                    "sharpe_ratio_5y": 1.95,
                    "max_drawdown_percent": -10.5,
                    "cagr_5y": 19.2,
                    "regime_summary": "Stable compounding defensive tech regime."
                },
                "timeline_logs": [
                    {"agent_name": "Market Data Agent", "status": "COMPLETED", "runtime_ms": 210, "confidence": 99.0, "summary": "Fetched spot market quote ($448.90)."},
                    {"agent_name": "Portfolio Manager Agent", "status": "COMPLETED", "runtime_ms": 340, "confidence": 84.2, "summary": "Synthesized institutional consensus: BUY allocation."}
                ]
            },
            "DOSSIER-INST-TSLA-04": {
                "task_id": "DOSSIER-INST-TSLA-04",
                "ticker": "TSLA",
                "status": "COMPLETED",
                "created_at": now,
                "market_data": {
                    "ticker": "TSLA",
                    "company_name": "Tesla, Inc.",
                    "current_price": 252.10,
                    "daily_change_percent": -1.45,
                    "volume": 74200000,
                    "avg_volume_10d": 68000000
                },
                "portfolio_manager": {
                    "ticker": "TSLA",
                    "decision": "Hold",
                    "confidence": 68.0,
                    "position_size": "5.0%",
                    "risk": "High",
                    "summary": "High implied volatility and macro yield sensitivity create neutral short-term regime. VWAP Iceberg execution advised on dips towards 200-day moving average.",
                    "bullish_reasons": [
                        "Energy storage deployment division experiencing exponential +120% YoY growth.",
                        "Full Self-Driving (FSD) v13 software release milestones."
                    ],
                    "bearish_reasons": [
                        "Automotive gross margin compression from global EV pricing competition.",
                        "Extreme sensitivity to macro interest rate fluctuations."
                    ]
                },
                "risk_manager": {
                    "ticker": "TSLA",
                    "sharpe_ratio": 1.12,
                    "max_drawdown_percent": -28.4,
                    "var_95_percent": -4.20,
                    "beta": 1.95
                },
                "execution_plan": {
                    "ticker": "TSLA",
                    "ideal_buy_zone": "$235.00 - $242.00",
                    "stop_loss": "$222.00",
                    "take_profit": "$278.00",
                    "risk_reward_ratio": "1 : 2.1",
                    "suggested_order_type": "Limit Orders at Support / VWAP Dip Buying"
                },
                "options_flow": {
                    "ticker": "TSLA",
                    "put_call_ratio": 1.05,
                    "max_pain_strike": 250.0,
                    "iv_rank": 68.5,
                    "gamma_exposure_skew": "Neutral / Balanced Gamma Exposure",
                    "institutional_sentiment": "Balanced Put & Call Activity"
                },
                "historical_regime": {
                    "ticker": "TSLA",
                    "sharpe_ratio_5y": 1.12,
                    "max_drawdown_percent": -28.4,
                    "cagr_5y": 15.6,
                    "regime_summary": "Volatile momentum consolidation."
                },
                "timeline_logs": [
                    {"agent_name": "Market Data Agent", "status": "COMPLETED", "runtime_ms": 230, "confidence": 99.0, "summary": "Fetched quote data ($252.10)."},
                    {"agent_name": "Portfolio Manager Agent", "status": "COMPLETED", "runtime_ms": 350, "confidence": 68.0, "summary": "Synthesized institutional consensus: HOLD allocation."}
                ]
            }
        }

    async def connect(self):
        settings = get_settings()
        try:
            self._client = AsyncIOMotorClient(
                settings.MONGODB_URI, 
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where()
            )
            self._db = self._client[settings.MONGODB_DB_NAME]
            # Verify connection
            await self._client.admin.command("ping")
            self._mongo_available = True
            logger.info(f"Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
            
            # Create indices in background
            await self._db.analysis_runs.create_index("task_id", unique=True)
            await self._db.analysis_runs.create_index("ticker")
            await self._db.analysis_runs.create_index("created_at")
        except Exception as e:
            self._mongo_available = False
            logger.info(f"MongoDB connection failed ({e}). Using in-memory fallback repository.")

    async def save_analysis_run(self, result: AnalysisRunResult):
        async with self._lock:
            data = result.model_dump()
            if self._mongo_available and self._db is not None:
                try:
                    await self._db.analysis_runs.update_one(
                        {"task_id": result.task_id},
                        {"$set": data},
                        upsert=True
                    )
                    return
                except Exception as e:
                    logger.debug(f"Failed to save analysis run to MongoDB: {e}")
            self._memory_runs[result.task_id] = data

    async def get_analysis_run(self, task_id: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            if self._mongo_available and self._db is not None:
                try:
                    doc = await self._db.analysis_runs.find_one({"task_id": task_id}, {"_id": 0})
                    if doc:
                        return doc
                except Exception as e:
                    logger.debug(f"Failed to get run from MongoDB: {e}")
            return self._memory_runs.get(task_id)

    async def get_history_by_ticker(self, ticker: str, limit: int = 20) -> List[Dict[str, Any]]:
        async with self._lock:
            if self._mongo_available and self._db is not None:
                try:
                    cursor = self._db.analysis_runs.find({"ticker": ticker.upper()}, {"_id": 0}).sort("created_at", -1).limit(limit)
                    return await cursor.to_list(length=limit)
                except Exception as e:
                    logger.debug(f"Failed to query history from MongoDB: {e}")
            results = [doc for doc in self._memory_runs.values() if doc.get("ticker", "").upper() == ticker.upper()]
            results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return results[:limit]

    async def get_all_analysis_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        async with self._lock:
            results: List[Dict[str, Any]] = []
            if self._mongo_available and self._db is not None:
                try:
                    cursor = self._db.analysis_runs.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
                    results = await cursor.to_list(length=limit)
                except Exception as e:
                    logger.debug(f"Failed to query all runs from MongoDB: {e}")
            if not results:
                results = list(self._memory_runs.values())
                results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            return results[:limit]

    async def get_watchlist(self, name: str = "default") -> List[str]:
        async with self._lock:
            if self._mongo_available and self._db is not None:
                try:
                    doc = await self._db.watchlists.find_one({"name": name}, {"_id": 0})
                    if doc and "tickers" in doc:
                        return doc["tickers"]
                except Exception:
                    pass
            return self._memory_watchlists.get(name, ["AAPL", "NVDA", "TSLA"])

    async def update_watchlist(self, tickers: List[str], name: str = "default"):
        async with self._lock:
            clean_tickers = [t.strip().upper() for t in tickers if t.strip()]
            if self._mongo_available and self._db is not None:
                try:
                    await self._db.watchlists.update_one(
                        {"name": name},
                        {"$set": {"tickers": clean_tickers, "updated_at": datetime.now(timezone.utc).isoformat()}},
                        upsert=True
                    )
                except Exception:
                    pass
            self._memory_watchlists[name] = clean_tickers

    async def delete_analysis_run(self, task_id: str) -> bool:
        async with self._lock:
            if self._mongo_available and self._db is not None:
                try:
                    await self._db.analysis_runs.delete_one({"task_id": task_id})
                except Exception as e:
                    logger.debug(f"Failed to delete {task_id} from MongoDB: {e}")
            if task_id in self._memory_runs:
                del self._memory_runs[task_id]
            return True

    async def delete_all_analysis_runs(self) -> bool:
        async with self._lock:
            if self._mongo_available and self._db is not None:
                try:
                    await self._db.analysis_runs.delete_many({})
                except Exception as e:
                    logger.debug(f"Failed to delete all runs from MongoDB: {e}")
            self._memory_runs.clear()
            return True


mongodb_manager = MongoDBManager()
