import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from fastapi import APIRouter, Request, Response
from protocol import Protocol
from database import Database
from internals.session_utils import handle_session, set_username_cookie

router = APIRouter()

db = Database.get_instance("users.db")

@router.post('/api/log-in')
async def log_in_with_email(request: Request, response: Response):
    info = await request.json()

    enc_email = info.get('email')
    enc_password = info.get('password')

    if not (enc_email and enc_password):
        return Protocol.Error.invalid_request

    client = handle_session(request, response)

    email, password = client.decrypt(enc_email), client.decrypt(enc_password)
    print(email, password)
    print(info)

    log_in_success = db.log_in(email, password)
    print(log_in_success)
    if log_in_success == Protocol.success:
        username = db.get_user_info_by_email(email)
        print("clienting", client.username)
        client.log_in(username)
        set_username_cookie(client, response)
        
    return {
        "success": log_in_success
    }


@router.post("/api/sign-up")
async def sign_up(request: Request, response: Response):
    client = handle_session(request, response)

    info = await request.json()

    username = info.get('username')
    country = info.get('country')
    email = info.get('email')
    password = info.get('password')

    if not (username and country and email and password):
        return Protocol.Error.invalid_request

    username = client.decrypt(username)
    country = client.decrypt(country)
    email = client.decrypt(email)
    password = client.decrypt(password)

    print(
        f"username: {username}, country: {country}, email: {email}, password: {password}"
    )

    sign_up_status = db.sign_up(username, country, email, password)
    if sign_up_status == Protocol.success:
        client.log_in(username)
        set_username_cookie(client, response)

        response = {
            "username": username
        }
    response["status"] = sign_up_status
    return response
