import { AsyncLock } from "./AsyncLock";

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
        await this.lock.acquire();
        try {
            return new Promise((resolve, reject) => {
                if (!this.socket) {
                    reject();
                    return
                }
                this.socket.onmessage = (response) => {
                    resolve(response.data);
                };
                this.socket?.send(request);
            });    
        } finally {
            this.lock.release();
        }
    }

    async send(request: string) {
        this.lock.acquire();
        try {
            this.socket?.send(request);
        } finally {
            this.lock.release();
        }
    }

    async receive(): Promise<string> {
        this.lock.acquire();
        try {
            return new Promise((resolve, reject) => {
                if (!this.socket) {
                    reject();
                    return
                }
    
                this.socket.onmessage = (response) => {
                    resolve(response.data);
                };
            })    
        } finally {
            this.lock.release();
        }
    }

    async disconnect() {
        this.socket?.close();
        this.socket = null;
    }
};
