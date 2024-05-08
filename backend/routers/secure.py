import sys
sys.path.append("..")  # Adds higher directory to python modules path.

import internals.encryption.rsa as rsa
from fastapi import APIRouter, Request, Response
from internals.session_utils import handle_session
from protocol import Protocol

public_key, private_key = rsa.get_keys()
router = APIRouter()

@router.get("/api/public-key")
def get_public_key():
    return {"key": public_key.export_key()}


@router.post("/api/handshake")
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
        return Protocol.success

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Failed to decrypt AES key") from e
