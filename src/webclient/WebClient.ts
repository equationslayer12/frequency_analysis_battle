import HTTPClient from "./HTTPClient";
import SessionHandle from "./Sessions/SessionHandle";
import SocketClient from "./SocketClient";


class WebClient {
    /**
     * Wrapper for HTTPClient and SocketClient and SessionHandle
     */
    http: HTTPClient;
    socket: SocketClient;
    sessions: SessionHandle;
    constructor() {
        this.http = new HTTPClient();
        this.socket = new SocketClient();
        this.sessions = SessionHandle;
    }
}

export default new WebClient();
