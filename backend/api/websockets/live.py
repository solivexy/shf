import logging
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.ws_manager import ws_manager

logger = logging.getLogger("api_websocket")
router = APIRouter(prefix="/ws", tags=["WebSockets"])


@router.websocket("/live/{task_id}")
async def websocket_live_endpoint(websocket: WebSocket, task_id: str):
    """
    Real-time WebSocket endpoint that streams agent execution timeline steps (`AgentTimelineLog`),
    status updates, and completed recommendation JSON to connected institutional dashboards.
    """
    await ws_manager.connect(websocket, task_id)
    try:
        while True:
            # Keep connection alive and receive ping/heartbeats from client if needed
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text('{"type": "pong"}')
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, task_id)
    except Exception as e:
        logger.debug(f"WebSocket connection {task_id} closed unexpectedly: {e}")
        await ws_manager.disconnect(websocket, task_id)
