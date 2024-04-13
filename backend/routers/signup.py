import sys
sys.path.append("..") # Adds higher directory to python modules path.

from fastapi import APIRouter, Request
from protocol import Protocol
from database import Database

router = APIRouter()

db = Database.get_instance("users.db")


@router.post('/api/log-in')
async def log_in_with_email(request: Request):
    info = await request.json()

    email = info.get('email')
    password = info.get('password')

    print(email, password)

    if not (email and password):
        return Protocol.Error.invalid_request

    log_in_success = db.log_in(email, password)

    return {
        "success": log_in_success
    }


@router.post("/api/sign-up")
async def sign_up(request: Request):
    info = await request.json()

    username = info.get('username')
    country = info.get('country')
    email = info.get('email')
    password = info.get('password')

    print(
        f"username: {username}, country: {country}, email: {email}, password: {password}"
    )

    if not (username and country and email and password):
        return Protocol.Error.invalid_request

    sign_up_status = db.sign_up(username, country, email, password)

    return {
        "success": sign_up_status
    }
