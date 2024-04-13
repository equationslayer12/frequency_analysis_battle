import sys
sys.path.append("..") # Adds higher directory to python modules path.

from .http_session import HTTPSession
from client import Client

clients: dict = {}

def handle_socket_session(websocket) -> Client:
    client: Client | None = None
    session_cookie = websocket.cookies.get('session')
    print(f"socket session cookie: {session_cookie}")
    if session_cookie is None:
        return None
    session = HTTPSession.decrypt(session_cookie)
    if not session:
        return None
    print("the key", session.key)
    client = clients.get(session.key)
    print(f"client: {client}")
    # print(f"ladies and gentleman client {client.nickname} connected!")

    return client


def handle_session(request, response) -> Client:
    client: Client | None = None
    session_cookie = request.cookies.get('session')
    client_is_connected = False
    print(f"session cookie: {session_cookie}")
    if session_cookie is not None:
        apply_easter_eggs(request, response)

        session = HTTPSession.decrypt(session_cookie)
        if session:
            client = clients.get(session.key)
            if client:
                client_is_connected = True
        # print(f"ladies and gentleman client {client.nickname} connected!")

    if not client_is_connected:
        new_session = HTTPSession(
            key=HTTPSession._generate_session_key(),
            expire=None
        )
        client = Client(new_session)
        clients[new_session.key] = client
        response.set_cookie(key="session", value=new_session.encrypt())
        print(f"created {client.nickname}, with key={client.session.key}")
    return client


def apply_easter_eggs(request, response):
    if request.cookies.get('easterEgg') is not None:
        response.set_cookie(key='easterEgg', value="Beer Sheva <3")
    if request.cookies.get('admin') is not None:
        response.set_cookie(
            key='admin', value='Depreciated Try setting cookie easterEgg instead.')
