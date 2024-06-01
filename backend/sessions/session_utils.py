import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from typing import Tuple
from fastapi import Request, Response
from .http_session import HTTPSession
from backend.web.web_client import WebClient


clients: dict = {}


def handle_socket_session(websocket) -> WebClient:
    client: WebClient | None = None
    session_cookie = websocket.cookies.get('session')
    if session_cookie is None:
        return None
    session = HTTPSession.decrypt_session(session_cookie)
    if not session:
        return None
    client = clients.get(session.key)

    client.socket = websocket
    return client


def handle_session(request: Request, response: Response) -> WebClient:
    """If a request contains cookies, extract the client from it.
    if it doesn't, create a client and a cookie and attach it to response.

    Args:
        request (Request): Client HTTP Request
        response (Response): Server HTTP Response

    Returns:
        WebClient: a class that represents a user web connection.
    """
    client: WebClient | None = None

    session_cookie = request.cookies.get('session')
    username_cookie = request.cookies.get('username')
    print(f"session cookie: {session_cookie}")
    print(f"username cookie: {username_cookie}")

    if session_cookie is not None:
        apply_easter_eggs(request, response)
        client = attempt_session_login(session_cookie)
        if not username_cookie:
            set_username_cookie(client, response)

    if client is None:
        new_session = HTTPSession(
            key=HTTPSession._generate_session_key(),
            expire=None,
        )
        client = WebClient(new_session)
        clients[new_session.key] = client

        new_session.set_username(client.username)

        response.set_cookie(key="session", value=new_session.encrypt_session())
        response.set_cookie(
            key="username", value=new_session.encrypt_username())
        print(f"created {client.username}, with key={client.session.key}")
    return client


def set_username_cookie(client: WebClient, response: Response):
    if client is None:
        return
    session = client.session
    if session is None:
        return
    client.session.set_username(client.username)
    response.set_cookie(key="username", value=session.encrypt_username())


def attempt_session_login(session_cookie: str) -> WebClient:
    session = HTTPSession.decrypt_session(session_cookie)
    client = clients.get(session.key)

    if not client:
        return None

    return client


def apply_easter_eggs(request, response):
    if request.cookies.get('easterEgg') is not None:
        response.set_cookie(key='easterEgg', value="Beer Sheva <3")
    if request.cookies.get('admin') is not None:
        response.set_cookie(
            key='admin', value='Depreciated Try setting cookie easterEgg instead.')
