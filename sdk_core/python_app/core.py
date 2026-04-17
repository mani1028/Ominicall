import asyncio
import json
import aiohttp
import datetime
from aiortc import RTCPeerConnection, RTCSessionDescription

class OmniCallApp:
    def __init__(self, user_id, signaling_url="ws://localhost:8000/ws"):
        self.user_id = user_id
        self.signaling_url = f"{signaling_url}/{user_id}"
        self.pc = RTCPeerConnection()

    async def start(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.signaling_url) as ws:
                print(f"🚀 Headless Client '{self.user_id}' is Online.")
                async for msg in ws:
                    data = json.loads(msg.data)
                    if data['type'] == 'offer':
                        await self._handle_offer(data, ws)

    async def _handle_offer(self, data, ws):
        print(f"📞 Connection request from: {data.get('sender')}")
        offer = RTCSessionDescription(sdp=data['sdp'], type='offer')
        await self.pc.setRemoteDescription(offer)

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            print(f"✅ Data Channel detected: {channel.label}")
            
            async def heartbeat():
                # Wait for the browser to be ready
                while channel.readyState != "open":
                    await asyncio.sleep(0.2)
                
                print(f"🔥 Channel {channel.label} is ACTIVE. Starting Heartbeat...")
                while channel.readyState == "open":
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    msg = f"Heartbeat from {self.user_id} at {now}"
                    channel.send(msg)
                    print(f"📤 Sent: {msg}")
                    await asyncio.sleep(5)

            asyncio.create_task(heartbeat())

        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        await ws.send_json({
            'type': 'answer',
            'target': data.get('sender'),
            'sdp': self.pc.localDescription.sdp
        })
        print("📤 Answer sent back.")