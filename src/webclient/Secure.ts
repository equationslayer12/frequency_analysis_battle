import * as CryptoJS from "crypto-js";
import JSEncrypt from "jsencrypt";

import HTTPClient from './HTTPClient';
import Protocol from './Protocol';

/**
 * Utility class for encryption and secure communication.
 */
export class Secure {
    /** The passphrase used for AES encryption. */
    aesPassphrase: string;

    /** The AES key used for encryption and decryption. */
    aesKey: CryptoJS.lib.WordArray;

    /** Indicates whether encryption is enabled. */
    isEnabled: boolean;

    /**
     * Constructs a new instance of the Secure class.
     * Initializes the AES passphrase and key.
     */
    constructor() {
        this.aesPassphrase = this._generateRandomString(32);
        this.aesKey = CryptoJS.enc.Utf8.parse(this.aesPassphrase);
        this.isEnabled = false;    
    }
    
    /**
     * Encrypts a message using AES encryption.
     * @param message The message to encrypt.
     * @returns The encrypted message.
     */
    encrypt(message: string): string {
        const encrypted = CryptoJS.AES.encrypt(message, this.aesKey, { mode: CryptoJS.mode.ECB })
        return encrypted.toString();
    }
    
    /**
     * Decrypts an encrypted message using AES decryption.
     * @param encrypted The encrypted message.
     * @returns The decrypted message.
     */
    decrypt(encrypted: string): string {
        const decrypted = CryptoJS.AES.decrypt(encrypted, this.aesKey, { mode: CryptoJS.mode.ECB })
        return decrypted.toString();    
    }
    
    /**
     * Performs a handshake with the server to establish secure communication.
     * Retrieves the server's public RSA key, encrypts the AES key with it,
     * and sends it to the server for validation.
     */
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

    /**
     * Generates a random string of the specified length.
     * @param length The length of the random string.
     * @returns The randomly generated string.
     * @private
     */
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
