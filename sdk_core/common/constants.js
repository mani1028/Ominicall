export const OMNI_CONFIG = {
    SILENT_KILLER_TIMEOUT: 5000, // 5 seconds of 0 bytes before recovery
    WATCHDOG_INTERVAL: 2000,     // Check stats every 2 seconds
    ICE_RESTART_DELAY: 1000,     // Wait 1s before trying to reconnect
    DEFAULT_STUN: "stun:stun.l.google.com:19302"
};

export const SIGNAL_TYPES = {
    OFFER: "offer",
    ANSWER: "answer",
    CANDIDATE: "candidate",
    RESTART: "ice-restart"
};