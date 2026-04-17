import asyncio

class HealthMonitor:
    def __init__(self, pc):
        self.pc = pc

    async def start_watchdog(self):
        print("[Health] Monitoring active...")
        last_bytes = 0
        
        while self.pc.iceConnectionState == "connected":
            stats = await self.pc.getStats()
            current_bytes = 0
            
            # Find the inbound audio stats
            for report in stats.values():
                if report.type == "inbound-rtp" and report.kind == "audio":
                    current_bytes = report.get("bytesReceived", 0)
            
            if current_bytes == last_bytes and last_bytes > 0:
                print("[Health] ALERT: Data frozen! Potential Silent Killer.")
            else:
                # Flowing normally
                pass
                
            last_bytes = current_bytes
            await asyncio.sleep(2)