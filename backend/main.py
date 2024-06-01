from fastapi import FastAPI, Request
from routers import signup, secure, freq_practice, freq_race, testing
from typing import Callable

app = FastAPI()

def main() -> None:
    app.include_router(signup.router)
    app.include_router(freq_practice.router)
    app.include_router(freq_race.router)
    app.include_router(secure.router)
    app.include_router(testing.router)

@app.middleware("http")
async def middleware(request: Request, call_next: Callable):
    """Middleware function to intercept incoming requests."""
    response = await call_next(request)
    return response


main()
