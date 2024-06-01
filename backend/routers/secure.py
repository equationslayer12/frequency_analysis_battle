import sys
sys.path.append("..")  # Adds higher directory to python modules path.

import sessions.encryption.rsa as rsa
from fastapi import APIRouter, Request, Response
from sessions.session_utils import handle_session
from backend.config.protocol import Protocol

public_key, private_key = rsa.get_keys()
router = APIRouter()

@router.get("/api/public-key")
def get_public_key():
    """
    Endpoint to retrieve the server's public key.

    Returns:
        dict: A dictionary containing the public key as a string.
    """
    return {"key": public_key.export_key()}


@router.post("/api/handshake")
async def handshake(request: Request, response: Response):
    """
    Endpoint to handle the initial handshake between client and server.
    This endpoint expects an encrypted AES key from the client,
    which it decrypts using the server's private key and sets for the client's session.

    Args:
        request (Request): The incoming HTTP request.
        response (Response): The outgoing HTTP response.

    Returns:
        dict: A dictionary indicating success or failure of the handshake process.

    Raises:
        HTTPException: If the AES key decryption fails.
    """
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
