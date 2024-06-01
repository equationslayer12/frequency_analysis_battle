import HTTPClient from './HTTPClient';
import SocketClient from './SocketClient';
import { Secure } from './Secure';

const secure = new Secure();
await secure.handshake();

/**
 * WebClient class acts as a wrapper for HTTPClient and SocketClient.
 * It also handles encryption of data sent using the Secure class.
 */
class WebClient {
     /** The WebSocket client for communication with the server. */
     socket: SocketClient;

     /**
      * Constructs a new instance of the WebClient class.
      * Initializes the SocketClient for WebSocket communication.
      */
     constructor() {
          this.socket = new SocketClient();
     }

     /**
      * Sends an HTTP GET request to the specified URL.
      * @param url The URL to send the request to.
      * @returns A promise that resolves with the response data from the server.
      */
     async APIRequest(url: string) {
          return await HTTPClient.APIRequest(url);
     }

     /**
      * Sends an HTTP POST request to the specified URL with the provided data.
      * If encryption is enabled, it encrypts the data before sending.
      * @param url The URL to send the request to.
      * @param data The data to send with the request.
      * @returns A promise that resolves with the response data from the server.
      */
     async APIRequestPost(url: string, data: { [key: string]: any }) {
          if (secure.isEnabled) {
               console.log('Encrypting data...');
               for (const [key, value] of Object.entries(data)) {
                    data[key] = secure.encrypt(value);
               }
          }
          return await HTTPClient.APIRequestPost(url, data);
     }
}

/** The instance of the WebClient class used for API communication. */
export const webClient = new WebClient();
