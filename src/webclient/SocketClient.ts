import { AsyncLock } from './AsyncLock';

export default class SocketClient {
     /** The WebSocket connection to the server. */
     socket: WebSocket | null;

     /** A lock to ensure thread safety when sending and receiving messages. */
     lock: AsyncLock;

     /**
      * Constructs a new instance of the SocketClient class.
      * Initializes the WebSocket connection and the async lock.
      */
     constructor() {
          this.socket = null;
          this.lock = new AsyncLock();
     }

     /**
      * Connects to the server WebSocket at the specified URL.
      * @param url The URL of the WebSocket server.
      * @returns A promise that resolves with the WebSocket connection when successfully connected.
      */
     async connectToServer(url: string) {
          return new Promise((resolve, reject) => {
               let ws = new WebSocket('ws://localhost:8080/api' + url);
               ws.onopen = (event) => {
                    console.log('Connected to server socket');
                    this.socket = ws;
                    resolve(ws);
               };
          });
     }

     /**
      * Checks if the client is currently connected to the server.
      * @returns True if the client is connected, otherwise false.
      */
     isConnected() {
          return this.socket != null;
     }

     /**
      * Sends a request to the server and waits for a response.
      * @param request The request message to send to the server.
      * @returns A promise that resolves with the response message received from the server.
      */
     async sendAndReceive(request: string): Promise<string> {
          await this.lock.acquire();
          try {
               return new Promise((resolve, reject) => {
                    if (!this.socket) {
                         reject();
                         return;
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

     /**
      * Sends a request to the server without waiting for a response.
      * @param request The request message to send to the server.
      */
     async send(request: string) {
          this.lock.acquire();
          try {
               this.socket?.send(request);
          } finally {
               this.lock.release();
          }
     }

     /**
      * Receives a message from the server.
      * @returns A promise that resolves with the message received from the server.
      */
     async receive(): Promise<string> {
          this.lock.acquire();
          try {
               return new Promise((resolve, reject) => {
                    if (!this.socket) {
                         reject();
                         return;
                    }

                    this.socket.onmessage = (response) => {
                         resolve(response.data);
                    };
               });
          } finally {
               this.lock.release();
          }
     }

     /**
      * Disconnects from the server WebSocket.
      */
     async disconnect() {
          this.socket?.close();
          this.socket = null;
     }
}
