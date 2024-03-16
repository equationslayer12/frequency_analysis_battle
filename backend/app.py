# from flask import Flask, jsonify
# from flask_cors import CORS
from fastapi import FastAPI, WebSocket, Request, Response
from typing import Dict
from race_game import RaceGame
from client import Client
from session import Session

app = FastAPI()
clients: dict = {}
# CORS(app, resources={r"*": {"origins": "*"}})

a = 0

@app.get('/')
def root():
    return {"message": "hello guys welcome to my youtube channel"}


@app.get("/api/practice")
def practice(request: Request, response: Response):
    client = handle_session(request, response)
    if not client.race_game:
        client.race_game = RaceGame()

    return {
        "text": client.race_game.ciphered_text
    }


@app.websocket("/api/practice")
async def practice_socket(websocket: WebSocket):
    await websocket.accept()
    client = handle_socket_session(websocket)
    client.socket = websocket


def handle_socket_session(websocket) -> Client:
    client: Client | None = None
    session_cookie = websocket.cookies.get('session')
    print(f"socket session cookie: {session_cookie}")
    if session_cookie is None:
        return None
    session = Session.decrypt(session_cookie)
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

        session = Session.decrypt(session_cookie)
        if session:
            client = clients.get(session.key)
            if client:
                client_is_connected = True
        # print(f"ladies and gentleman client {client.nickname} connected!")

    if not client_is_connected:
        new_session = Session(
            key=Session._generate_session_key(),
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


@app.get("/api/test_socket")
def test_socket_http():
    return "This is a real request thank you"


@app.websocket("/api/test_socket_test")
async def test_socket(websocket: WebSocket):
    await websocket.accept()

    text1 = await websocket.receive_text()
    print(text1)
    text2 = await websocket.receive_text()
    print(text2)
    await websocket.send_text("GET SCAMMED")


@app.post("/api/test")
def test():
    global a
    a += 1
    return str(a)


@app.get("/api/test")
def get_test():
    return str(a)
