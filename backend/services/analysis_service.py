import uuid
import time
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from models.state import HedgeFundState
from models.schemas import AnalysisRunResult, AgentTimelineLog
from workflows.hedge_fund_graph import build_hedge_fund_graph
from database.mongodb import mongodb_manager
from services.ws_manager import ws_manager

logger = logging.getLogger("analysis_service")


class AnalysisService:
    """
    Orchestrates multi-agent analysis runs asynchronously, maintains database sync,
    and broadcasts real-time timeline steps over WebSockets.
    """
    def __init__(self):
        self.active_tasks: Dict[str, AnalysisRunResult] = {}

    async def start_analysis_job(self, ticker: str, task_id: Optional[str] = None) -> AnalysisRunResult:
        if not task_id:
            task_id = f"task_{uuid.uuid4().hex[:12]}"

        ticker = ticker.upper().strip()
        logger.info(f"Initiating multi-agent analysis job {task_id} for ticker: {ticker}")

        initial_result = AnalysisRunResult(
            task_id=task_id,
            ticker=ticker,
            status="RUNNING",
            timeline_logs=[
                AgentTimelineLog(agent_name="Market Data Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Historical Regime Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Technical Analysis Agent", status="PENDING"),
                AgentTimelineLog(agent_name="News Intelligence Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Macro Economy Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Options Flow Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Risk Manager Agent", status="PENDING"),
                AgentTimelineLog(agent_name="ML Prediction Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Portfolio Manager Agent", status="PENDING"),
                AgentTimelineLog(agent_name="Execution Agent", status="PENDING"),
            ]
        )

        self.active_tasks[task_id] = initial_result
        await mongodb_manager.save_analysis_run(initial_result)
        await ws_manager.broadcast_to_task(task_id, {"type": "ANALYSIS_STARTED", "data": initial_result.model_dump()})

        # Launch background task
        asyncio.create_task(self._run_graph_loop(task_id, ticker))
        return initial_result

    async def _run_graph_loop(self, task_id: str, ticker: str):
        async def step_callback(state: HedgeFundState, node_name: str):
            # Update active task result
            run_res = self._state_to_run_result(task_id, ticker, "RUNNING", state)
            self.active_tasks[task_id] = run_res
            await mongodb_manager.save_analysis_run(run_res)
            await ws_manager.broadcast_to_task(task_id, {
                "type": "STEP_COMPLETED",
                "node": node_name,
                "data": run_res.model_dump()
            })
            await asyncio.sleep(0.1)  # small yield for websocket delivery

        try:
            graph = build_hedge_fund_graph(step_callback=step_callback)
            initial_state: HedgeFundState = {
                "task_id": task_id,
                "ticker": ticker,
                "status": "RUNNING",
                "timeline_logs": [
                    AgentTimelineLog(agent_name="Market Data Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Historical Regime Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Technical Analysis Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="News Intelligence Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Macro Economy Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Options Flow Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Risk Manager Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="ML Prediction Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Portfolio Manager Agent", status="PENDING"),
                    AgentTimelineLog(agent_name="Execution Agent", status="PENDING"),
                ]
            }

            final_state = await graph.ainvoke(initial_state)
            final_status = "FAILED" if final_state.get("error") else "COMPLETED"
            final_res = self._state_to_run_result(task_id, ticker, final_status, final_state)
            
            self.active_tasks[task_id] = final_res
            await mongodb_manager.save_analysis_run(final_res)
            await ws_manager.broadcast_to_task(task_id, {
                "type": "ANALYSIS_COMPLETED",
                "data": final_res.model_dump()
            })
            logger.info(f"Analysis job {task_id} completed successfully for {ticker}.")

        except Exception as e:
            logger.error(f"Analysis job {task_id} encountered fatal error: {e}")
            if task_id in self.active_tasks:
                self.active_tasks[task_id].status = "FAILED"
                await mongodb_manager.save_analysis_run(self.active_tasks[task_id])
                await ws_manager.broadcast_to_task(task_id, {
                    "type": "ANALYSIS_FAILED",
                    "error": str(e),
                    "data": self.active_tasks[task_id].model_dump()
                })

    def _state_to_run_result(self, task_id: str, ticker: str, status: str, state: HedgeFundState) -> AnalysisRunResult:
        return AnalysisRunResult(
            task_id=task_id,
            ticker=ticker,
            status=status,
            timeline_logs=state.get("timeline_logs", []),
            market_data=state.get("market_data"),
            historical_regime=state.get("historical_regime"),
            technical_analysis=state.get("technical_analysis"),
            news_intelligence=state.get("news_intelligence"),
            macro_economy=state.get("macro_economy"),
            options_flow=state.get("options_flow"),
            risk_manager=state.get("risk_manager"),
            ml_prediction=state.get("ml_prediction"),
            portfolio_manager=state.get("portfolio_manager"),
            execution_plan=state.get("execution_plan")
        )

    async def get_task_status(self, task_id: str) -> Optional[AnalysisRunResult]:
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        doc = await mongodb_manager.get_analysis_run(task_id)
        if doc:
            try:
                return AnalysisRunResult(**doc)
            except Exception:
                pass
        return None

    async def get_history(self, ticker: str) -> List[Dict[str, Any]]:
        return await mongodb_manager.get_history_by_ticker(ticker)

    async def get_all_reports(self, limit: int = 50) -> List[Dict[str, Any]]:
        return await mongodb_manager.get_all_analysis_runs(limit=limit)


analysis_service = AnalysisService()
