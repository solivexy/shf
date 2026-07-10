import time
import logging
from typing import Callable, Any, Coroutine
from models.state import HedgeFundState
from models.schemas import AgentTimelineLog

logger = logging.getLogger("base_agent")


def emit_timeline_log(
    state: HedgeFundState,
    agent_name: str,
    status: str,
    runtime_ms: float = 0.0,
    confidence: float = None,
    summary: str = None,
    reasoning: str = None,
    output_json: Any = None
):
    """
    Appends or updates an agent's timeline execution log in the global state.
    Used by WebSocket broadcaster to stream real-time progress to the frontend dashboard.
    """
    if "timeline_logs" not in state or state["timeline_logs"] is None:
        state["timeline_logs"] = []

    # Check if agent already has an entry
    for entry in state["timeline_logs"]:
        if entry.agent_name == agent_name:
            entry.status = status
            if runtime_ms > 0:
                entry.runtime_ms = round(runtime_ms, 2)
            if confidence is not None:
                entry.confidence = confidence
            if summary is not None:
                entry.summary = summary
            if reasoning is not None:
                entry.reasoning = reasoning
            if output_json is not None:
                entry.output_json = output_json if isinstance(output_json, dict) else output_json.model_dump()
            return

    # Otherwise append new
    log_entry = AgentTimelineLog(
        agent_name=agent_name,
        status=status,
        runtime_ms=round(runtime_ms, 2),
        confidence=confidence,
        summary=summary,
        reasoning=reasoning,
        output_json=output_json if isinstance(output_json, dict) else (output_json.model_dump() if hasattr(output_json, "model_dump") else None)
    )
    state["timeline_logs"].append(log_entry)
