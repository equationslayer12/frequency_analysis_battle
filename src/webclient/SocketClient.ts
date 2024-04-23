export default class SocketClient {
    socket: WebSocket | null;
    constructor() {
        this.socket = null;
    }

    connectToServer() {
        let ws = new WebSocket('ws://localhost:8080/api/practice')
        ws.onopen = (event) => {
            console.log("Connected to server socket");
            this.socket = ws;
        };
    }
    
    isConnected() {
        return this.socket != null;
    }

    async sendAndReceive(request: string): Promise<string> {        
        return new Promise((resolve, reject) => {
            if (this.socket == null) {
                reject();
                return
            }
            this.socket.onmessage = (response) => {
                resolve(response.data);
            };
            this.send(request);
        });
    }

    async send(request: string) {
        this.socket?.send(request);
    }

    async disconnect() {
        this.socket?.close();
        this.socket = null;
    }
};
