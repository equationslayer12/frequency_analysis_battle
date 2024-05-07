import HTTPClient from "./HTTPClient";
import SessionHandle from "./Sessions/SessionHandle";
import SocketClient from "./SocketClient";
import {Secure} from "./Secure";

const secure = new Secure();
await secure.handshake();

class WebClient {
    /**
     * Wrapper for HTTPClient and SocketClient and SessionHandle
     * also encrypts the data sent
     */
    socket: SocketClient;
    constructor() {
        this.socket = new SocketClient();
    }

    async APIRequest(url: string) {
        return await HTTPClient.APIRequest(url)
    }
    async APIRequestPost(url: string, data: { [key: string]: any }) {
        if (secure.isEnabled) {
            console.log("encrypting tho...")
            for (const [key, value] of Object.entries(data)) {
                data[key] = secure.encrypt(value);
            }
        }
        return await HTTPClient.APIRequestPost(url, data)
    }

}   

export const webClient = new WebClient();
