from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.loop = None

    def set_loop(self, loop):
        self.loop = loop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_event(self, event_data: dict):
        # Broadcast standard event dictionary
        for connection in list(self.active_connections):
            try:
                await connection.send_json(event_data)
            except Exception as e:
                logger.debug(f"Error broadcasting event: {e}")

    def broadcast_sync(self, event_data: dict):
        """Thread-safe synchronous broadcast callable from Webots simulation thread."""
        if not self.active_connections:
            return
        import asyncio
        try:
            target_loop = self.loop
            if not target_loop:
                try:
                    target_loop = asyncio.get_event_loop()
                except Exception:
                    target_loop = None
            if target_loop and target_loop.is_running():
                asyncio.run_coroutine_threadsafe(self.broadcast_event(event_data), target_loop)
        except Exception:
            pass

manager = ConnectionManager()

@router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect much incoming traffic, just keeping connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
