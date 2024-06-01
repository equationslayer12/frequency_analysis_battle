import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def get_keys(size=1024):
    """
    Generate a pair of RSA keys (public and private).

    Args:
        size (int, optional): The key size in bits. Defaults to 1024. Minimum value is 1024.

    Returns:
        tuple: A tuple containing the public key and private key.
    """
    size = max(size, 1024)
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    return public_key, private_key

def encrypt(pubKey, msg):
    """
    Encrypt a message using the provided RSA public key.

    Args:
        pubKey (RSA.RsaKey): The RSA public key for encryption.
        msg (str): The plain text message to encrypt.

    Returns:
        bytes: The base64 encoded encrypted message.
    """
    msg = msg.encode()
    encryptor = PKCS1_v1_5.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    parsed = base64.b64encode(encrypted)
    return parsed

def decrypt(priKey, encrypted):
    """
    Decrypt an encrypted message using the provided RSA private key.

    Args:
        priKey (RSA.RsaKey): The RSA private key for decryption.
        encrypted (bytes): The base64 encoded encrypted message.

    Returns:
        bytes: The decrypted plain text message.
    """
    parsed = base64.b64decode(encrypted)
    decryptor = PKCS1_v1_5.new(priKey)
    decrypted = decryptor.decrypt(parsed, sentinel=None)
    return decrypted

if __name__ == '__main__':
    """
    Main method to demonstrate RSA key generation, encryption, and decryption.
    """
    pubKey, priKey = get_keys()
    message = "This is a secret message."

    encrypted_message = encrypt(pubKey, message)
    print(f"Encrypted: {encrypted_message}")

    decrypted_message = decrypt(priKey, encrypted_message)
    print(f"Decrypted: {decrypted_message.decode('utf-8')}")
