from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        # Overwrite if same user connects (prevents ghosts)
        self.active_connections[user_id] = websocket
        print(f"✅ {user_id} is now Online")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ {user_id} went Offline")

    async def forward_signal(self, data: dict, sender_id: str):
        target_id = data.get("target")
        if target_id in self.active_connections:
            data["sender"] = sender_id # Ensure receiver knows who called
            await self.active_connections[target_id].send_json(data)
            print(f"📨 {data['type']} forwarded: {sender_id} -> {target_id}")
        else:
            print(f"⚠️ {target_id} not found!")

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.forward_signal(data, user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)