from fastapi import FastAPI, Request, Response, WebSocket, HTTPException
from protocol import Protocol
from routers import signup, freqrace, testing
from typing import Callable
from internals.session_utils import handle_session
import internals.encryption.rsa as rsa
import internals.encryption.aes as aes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = FastAPI()


def main() -> None:
    app.include_router(signup.router)
    app.include_router(freqrace.router)
    app.include_router(testing.router)


public_key, private_key = rsa.get_keys()

@app.middleware("http")
async def middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    return response


@app.get("/api/public-key")
def get_public_key():
    return {"key": public_key.export_key()}

@app.post("/api/handshake")
async def handshake(request: Request, response: Response):
    info = await request.json()
    encrypted_aes_key = info.get("encrypted_aes_key")
    if not encrypted_aes_key:
        return
    client = handle_session(request, response)
    try:
        # Decrypt AES key with server's private key
        aes_key = rsa.decrypt(private_key, encrypted_aes_key).decode('utf-8')
        client.set_aes_key(aes_key)
        print("this is the aes key")
        print(aes_key)
        return Protocol.success
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Failed to decrypt AES key") from e


    # print(private_key)
    # print(client_encrypted_aes_key)

    # decryptor = PKCS1_OAEP.new(private_key)
    # decrypted = decryptor.decrypt(base64.b64decode(client_encrypted_aes_key))
    # print(decrypted)
    
    # # aes_key = public_key.decrypt(base64.b64decode(client_encrypted_aes_key))
    # # print(aes_key)
    # return "shitting"
    # AESC = aes.AESCipher(aes_key)
    # client.set_aesc(AESC)

main()
