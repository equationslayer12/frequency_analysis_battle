import axios from "axios";

export default class HTTPClient {
    static async APIRequest(url: string) {
        const response = await axios.get("/api" + url);
        return response?.data;
    }
    static async APIRequestPost(url: string, data: object) {
        const response = await axios.post("/api" + url, data);
        return response?.data;
    }    
};
