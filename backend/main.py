from fastapi import FastAPI, Request
from routers import signup, freqrace, secure, testing
from typing import Callable
from internals.session_utils import handle_session
import internals.encryption.aes as aes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = FastAPI()


def main() -> None:
    app.include_router(signup.router)
    app.include_router(freqrace.router)
    app.include_router(secure.router)
    app.include_router(testing.router)

@app.middleware("http")
async def middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    return response


main()
