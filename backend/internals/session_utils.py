import sys
sys.path.append("..")  # Adds higher directory to python modules path.

from client import Client
from .http_session import HTTPSession
from fastapi import Request, Response
from typing import Tuple

clients: dict = {}


def handle_socket_session(websocket) -> Client:
    client: Client | None = None
    session_cookie = websocket.cookies.get('session')
    print(f"socket session cookie: {session_cookie}")
    if session_cookie is None:
        return None
    session = HTTPSession.decrypt_session(session_cookie)
    if not session:
        return None
    print("the key", session.key)
    client = clients.get(session.key)
    print(f"client: {client}")
    # print(f"ladies and gentleman client {client.nickname} connected!")

    return client


def handle_session(request: Request, response: Response) -> Client:
    client: Client | None = None

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
        client = Client(new_session)
        clients[new_session.key] = client

        new_session.set_username(client.username)

        response.set_cookie(key="session", value=new_session.encrypt_session())
        response.set_cookie(key="username", value=new_session.encrypt_username())
        print(f"created {client.username}, with key={client.session.key}")
    return client

def set_username_cookie(client: Client, response: Response):
    if client is None:
        return
    session = client.session
    if session is None:
        return
    client.session.set_username(client.username)
    response.set_cookie(key="username", value=session.encrypt_username())

def attempt_session_login(session_cookie: str) -> Client:
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
