import { SignalingClient } from './signaling.js';

/**
 * OmniCall Headless SDK
 * A universal WebRTC wrapper for voice communication.
 */
export class OmniCall {
    constructor(config) {
        if (!config.userId || !config.serverUrl) {
            throw new Error("OmniCall: userId and serverUrl are required.");
        }

        this.userId = config.userId;
        this.state = 'IDLE'; 
        this.targetId = null;
        
        this.callbacks = {
            onIncoming: config.onIncoming || (() => {}),
            onAccepted: config.onAccepted || (() => {}),
            onHangup: config.onHangup || (() => {}),
            onBusy: config.onBusy || (() => {}),
            onReady: config.onReady || (() => {})
        };

        this.signaling = new SignalingClient(`${config.serverUrl}/ws/${this.userId}`);
        this.pc = null;
        this.localStream = null;
        this.pendingOffer = null;
        this.iceQueue = [];

        this._listen();
    }

    _listen() {
        this.signaling.onMessage = async (msg) => {
            switch (msg.type) {
                case 'offer':
                    if (this.state !== 'IDLE') {
                        this.signaling.send({ type: 'busy', target: msg.sender });
                    } else {
                        this.pendingOffer = msg;
                        this.callbacks.onIncoming(msg.sender);
                    }
                    break;
                case 'answer':
                    if (this.pc) {
                        await this.pc.setRemoteDescription(new RTCSessionDescription(msg));
                        this.state = 'BUSY';
                        await this._flushIce();
                        this.callbacks.onAccepted();
                    }
                    break;
                case 'candidate':
                    if (this.pc && this.pc.remoteDescription) {
                        this.pc.addIceCandidate(new RTCIceCandidate(msg.candidate)).catch(() => {});
                    } else {
                        this.iceQueue.push(msg.candidate);
                    }
                    break;
                case 'busy':
                    this.callbacks.onBusy();
                    this.cleanup();
                    break;
                case 'hangup':
                    this.cleanup();
                    this.callbacks.onHangup();
                    break;
            }
        };
    }

    async connect() {
        await this.signaling.connect();
        this.callbacks.onReady();
    }

    async _flushIce() {
        while (this.iceQueue.length > 0) {
            await this.pc.addIceCandidate(new RTCIceCandidate(this.iceQueue.shift())).catch(() => {});
        }
    }

    async _setup(targetId) {
        // Standard Google STUN server for P2P discovery
        this.pc = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });

        this.pc.onicecandidate = (e) => {
            if (e.candidate) {
                this.signaling.send({ type: 'candidate', target: targetId, candidate: e.candidate });
            }
        };

        this.pc.ontrack = (e) => {
            let audio = document.getElementById('omni-audio-stream');
            if (!audio) {
                audio = document.createElement('audio');
                audio.id = 'omni-audio-stream';
                audio.autoplay = true;
                document.body.appendChild(audio);
            }
            audio.srcObject = e.streams[0];
        };

        this.localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.localStream.getTracks().forEach(t => this.pc.addTrack(t, this.localStream));
    }

    async startCall(targetId) {
        this.state = 'CONNECTING';
        this.targetId = targetId;
        await this._setup(targetId);
        const offer = await this.pc.createOffer();
        await this.pc.setLocalDescription(offer);
        this.signaling.send({ type: 'offer', target: targetId, sdp: offer.sdp, sender: this.userId });
    }

    async acceptCall() {
        if (!this.pendingOffer) return;
        this.targetId = this.pendingOffer.sender;
        await this._setup(this.targetId);
        await this.pc.setRemoteDescription(new RTCSessionDescription(this.pendingOffer));
        const answer = await this.pc.createAnswer();
        await this.pc.setLocalDescription(answer);
        this.signaling.send({ type: 'answer', target: this.targetId, sdp: this.pc.localDescription.sdp });
        await this._flushIce();
        this.state = 'BUSY';
    }

    hangup() {
        if (this.targetId) this.signaling.send({ type: 'hangup', target: this.targetId });
        this.cleanup();
    }

    cleanup() {
        this.state = 'IDLE';
        if (this.localStream) {
            this.localStream.getTracks().forEach(t => t.stop());
            this.localStream = null;
        }
        if (this.pc) {
            this.pc.close();
            this.pc = null;
        }
        this.targetId = null;
        this.pendingOffer = null;
        const node = document.getElementById('omni-audio-stream');
        if (node) node.remove();
    }
}