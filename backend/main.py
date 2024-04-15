from fastapi import FastAPI, WebSocket
from protocol import Protocol
from routers import signup, freqrace, testing

app = FastAPI()

def main() -> None:
    app.include_router(signup.router)
    app.include_router(freqrace.router)
    app.include_router(testing.router)


main()
