import * as CryptoJS from "crypto-js";
import JSEncrypt from "jsencrypt";

import HTTPClient from './HTTPClient';
import Protocol from './Protocol';

export class Secure {
    aesPassphrase: string;
    aesKey: CryptoJS.lib.WordArray;
    isEnabled: boolean;

    constructor() {
        this.aesPassphrase = this._generateRandomString(32);
        console.log(this.aesPassphrase);
        this.aesKey = CryptoJS.enc.Utf8.parse(this.aesPassphrase);
        
        this.isEnabled = false;    
    }
    
    encrypt(message: string): string {
        const encrypted = CryptoJS.AES.encrypt(message, this.aesKey, { mode: CryptoJS.mode.ECB })
        return encrypted.toString();
    }
    
    decrypt(encrypted: string): string {
        const decrypted = CryptoJS.AES.decrypt(encrypted, this.aesKey, { mode: CryptoJS.mode.ECB })
        return decrypted.toString();    
    }
    
    async handshake() {
        // Get public server RSA key
        const SERVER_PUBLIC_KEY = (await HTTPClient.APIRequest("/public-key"))?.key;
        if (!SERVER_PUBLIC_KEY)
            return
    
        // Encrypt the AES key with the public server RSA key
        const encrypt = new JSEncrypt();
        encrypt.setPublicKey(SERVER_PUBLIC_KEY);
        const encryptedAesKey = encrypt.encrypt(this.aesPassphrase);
        
        // Send to server
        const response = await HTTPClient.APIRequestPost("/handshake", {encrypted_aes_key: encryptedAesKey});

        this.isEnabled = response == Protocol.success;
    }

    _generateRandomString(length: number) {
        let result = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        
        for (let i = 0; i < length; i++) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        
        return result;
    }
            
}
