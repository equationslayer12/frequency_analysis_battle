from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

"""
the client side uess AES ECB padding.
https://cryptojs.gitbook.io/docs#block-modes-and-padding
"""
class AESCipher(object):
    """AES encrypt and dcrypt"""

    def __init__(self, key: str):
        """
        Args:
            key (str): plain text AES key
        """
        self.block_size = AES.block_size
        self.key: bytes = key.encode('utf-8')

    def encrypt(self, message: str) -> bytes:
        padded = pad(message.encode('utf-8'), self.block_size)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(padded)
        return b64encode(encrypted)

    def decrypt(self, encrypted_text: str) -> str:
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_text)
        raw_data = unpad(decrypted, block_size=self.block_size)
        return raw_data.decode('utf-8')


if __name__ == "__main__":
    ...
