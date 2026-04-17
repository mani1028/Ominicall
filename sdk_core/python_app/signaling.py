import aiohttp
import json
import asyncio

class SignalingClient:
    def __init__(self, url, on_message):
        self.url = url
        self.on_message = on_message
        self.ws = None
        asyncio.create_task(self._listen())

    async def _listen(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.url) as ws:
                self.ws = ws
                print(f"[Signaling] Connected to {self.url}")
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await self.on_message(json.loads(msg.data))

    async def send(self, data):
        if self.ws:
            await self.ws.send_json(data)