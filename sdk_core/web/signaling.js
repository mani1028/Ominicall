export class SignalingClient {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.onMessage = null; // This is the placeholder
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(this.url);
            
            this.socket.onopen = () => {
                console.log("Connected to Signaling Server");
                resolve();
            };

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                // Check if the placeholder has been filled with a function
                if (this.onMessage) {
                    this.onMessage(data);
                }
            };

            this.socket.onerror = (err) => reject(err);
        });
    }

    send(data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        }
    }
}