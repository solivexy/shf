import asyncio
import json
import logging
from typing import Dict, List, Any
from fastapi import WebSocket

logger = logging.getLogger("ws_manager")


class ConnectionManager:
    """
    WebSocket Connection Manager.
    Maps task_id (or 'broadcast') to active client WebSocket connections and streams live agent timeline updates.
    """
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        async with self.lock:
            if task_id not in self.active_connections:
                self.active_connections[task_id] = []
            self.active_connections[task_id].append(websocket)
            logger.info(f"WebSocket client connected for task_id: {task_id}. Total: {len(self.active_connections[task_id])}")

    async def disconnect(self, websocket: WebSocket, task_id: str):
        async with self.lock:
            if task_id in self.active_connections:
                if websocket in self.active_connections[task_id]:
                    self.active_connections[task_id].remove(websocket)
                if not self.active_connections[task_id]:
                    del self.active_connections[task_id]
            logger.info(f"WebSocket client disconnected for task_id: {task_id}")

    async def broadcast_to_task(self, task_id: str, message: Dict[str, Any]):
        serialized = json.dumps(message, default=str)
        async with self.lock:
            sockets = self.active_connections.get(task_id, []) + self.active_connections.get("broadcast", [])
            for ws in list(set(sockets)):
                try:
                    await ws.send_text(serialized)
                except Exception as e:
                    logger.debug(f"Failed sending WebSocket message to {task_id}: {e}")


ws_manager = ConnectionManager()
