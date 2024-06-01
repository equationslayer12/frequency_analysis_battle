import axios, { AxiosResponse } from 'axios';

/**
 * Utility class for making HTTP requests.
 */
export default class HTTPClient {
     /**
      * Sends a GET request to the specified API endpoint.
      * @param url The API endpoint URL.
      * @returns A Promise that resolves to the response data from the server.
      */
     static async APIRequest(url: string): Promise<any> {
          const response = await axios.get('/api' + url);
          return response?.data;
     }

     /**
      * Sends a POST request to the specified API endpoint with the provided data.
      * @param url The API endpoint URL.
      * @param data The data to be sent in the request body.
      * @returns A Promise that resolves to the response data from the server.
      */
     static async APIRequestPost(url: string, data: object): Promise<any> {
          const response = await axios.post('/api' + url, data);
          return response?.data;
     }
}
