from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        # Maps user_id to their active WebSocket
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_to_user(self, message: dict, target_id: str):
        if target_id in self.active_connections:
            await self.active_connections[target_id].send_json(message)

manager = ConnectionManager()