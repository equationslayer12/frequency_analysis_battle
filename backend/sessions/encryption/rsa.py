import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def get_keys(size=1024):
    size = max(size, 1024)
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    return public_key, private_key

def encrypt(pubKey, msg):
    msg = msg.encode()
    encryptor = PKCS1_v1_5.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    parsed = base64.b64encode(encrypted)
    return parsed

def decrypt(priKey, encrypted):
    parsed = base64.b64decode(encrypted)

    decryptor = PKCS1_v1_5.new(priKey)
    decrypted = decryptor.decrypt(parsed, sentinel=None)
    return decrypted


if __name__ == '__main__':
    pubKey, priKey = get_keys()
