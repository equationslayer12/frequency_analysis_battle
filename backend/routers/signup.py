import sys
sys.path.append("..") # Adds higher directory to python modules path.

from fastapi import APIRouter, Request, Response
from protocol import Protocol
from database import Database
from internals.session_utils import handle_session, set_username_cookie

router = APIRouter()

db = Database.get_instance("users.db")

@router.post('/api/log-in')
async def log_in_with_email(request: Request, response: Response):
    info = await request.json()

    email = info.get('email')
    password = info.get('password')

    print(email, password)

    if not (email and password):
        return Protocol.Error.invalid_request

    log_in_success = db.log_in(email, password)
    if log_in_success == Protocol.success:
        username = db.get_user_info_by_email(email)
        client = handle_session(request, response)
        print("clienting", client)
        client.log_in(username)
        set_username_cookie(client, response)
        
    return {
        "success": log_in_success
    }


@router.post("/api/sign-up")
async def sign_up(request: Request, response: Response):
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
    if sign_up_status == Protocol.success:
        client = handle_session(request, response)
        client.log_in(username)
        set_username_cookie(client, response)

        response = {
            "username": username
        }
    response["status"] = sign_up_status
    return response
