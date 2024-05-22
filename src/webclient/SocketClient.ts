export default class SocketClient {
    socket: WebSocket | null;
    lock: AsyncLock
    constructor() {
        this.socket = null;
        this.lock = new AsyncLock();
    }

    async connectToServer(url: string) {
        return new Promise((resolve, reject) => {
            let ws = new WebSocket('ws://localhost:8080/api' + url)
            ws.onopen = (event) => {
                console.log("Connected to server socket");
                this.socket = ws;
                resolve(ws);
            };    
        })
    }
    
    isConnected() {
        return this.socket != null;
    }

    async sendAndReceive(request: string): Promise<string> {        
        return new Promise((resolve, reject) => {
            if (!this.socket) {
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

    async receive(): Promise<string> {
        return new Promise((resolve, reject) => {
            if (!this.socket) {
                reject();
                return
            }

            this.socket.onmessage = (response) => {
                resolve(response.data);
            };
        })
    }

    async disconnect() {
        this.socket?.close();
        this.socket = null;
    }
};
