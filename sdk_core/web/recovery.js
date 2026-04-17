export async function triggerRecovery(pc, targetId, signalingClient) {
    console.log(`[Recovery] Attempting ICE Restart for target: ${targetId}`);
    
    try {
        // This tells WebRTC to generate new credentials and ports
        const offer = await pc.createOffer({ iceRestart: true });
        await pc.setLocalDescription(offer);
        
        signalingClient.send({
            type: "offer",
            target: targetId,
            sdp: offer
        });
        
        console.log("[Recovery] ICE Restart Offer sent.");
    } catch (error) {
        console.error("[Recovery] Failed to restart ICE:", error);
    }
}