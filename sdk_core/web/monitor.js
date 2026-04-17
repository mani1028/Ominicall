export function startWatchdog(pc) {
    const interval = setInterval(async () => {
        const stats = await pc.getStats();
        let audioActive = false;
        stats.forEach(report => {
            if (report.type === 'inbound-rtp' && report.kind === 'audio') {
                if (report.bytesReceived > 0) audioActive = true;
            }
        });

        if (!audioActive) {
            console.warn("SILENT KILLER DETECTED: No audio packets moving.");
            // In a real 15-year dev scenario, we would trigger an ICE Restart here
        }
    }, 2000);
}