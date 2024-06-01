from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

"""
The client side uses AES ECB padding.
https://cryptojs.gitbook.io/docs#block-modes-and-padding
"""

class AESCipher(object):
    """Class for AES encryption and decryption using ECB mode with padding."""

    def __init__(self, key: str):
        """
        Initialize the AESCipher with a key.

        Args:
            key (str): Plain text AES key.
        """
        self.block_size = AES.block_size
        self.key: bytes = key.encode('utf-8')

    def encrypt(self, message: str) -> bytes:
        """
        Encrypt a message using AES encryption.

        Args:
            message (str): The plain text message to encrypt.

        Returns:
            bytes: The base64 encoded encrypted message.
        """
        padded = pad(message.encode('utf-8'), self.block_size)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(padded)
        return b64encode(encrypted)

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt an encrypted message using AES decryption.

        Args:
            encrypted_text (str): The base64 encoded encrypted message to decrypt.

        Returns:
            str: The decrypted plain text message.
        """
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_text)
        raw_data = unpad(decrypted, block_size=self.block_size)
        return raw_data.decode('utf-8')


if __name__ == "__main__":
    # Example usage (this part can be expanded as needed for testing)
    key = "mysecretpassword"
    cipher = AESCipher(key)

    original_message = "This is a secret message."
    encrypted_message = cipher.encrypt(original_message)
    print(f"Encrypted: {encrypted_message}")

    decrypted_message = cipher.decrypt(encrypted_message)
    print(f"Decrypted: {decrypted_message}")
