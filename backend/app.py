# from flask import Flask, jsonify
# from flask_cors import CORS
from fastapi import FastAPI, WebSocket, Request, Response
from typing import Dict
from race_game import RaceGame
from client import Client
from session import Session
from protocol import Protocol
from database import Database
from starlette.websockets import WebSocketDisconnect


app = FastAPI()
clients: dict = {}
db = Database.get_instance("users.db")
# CORS(app, resources={r"*": {"origins": "*"}})

a = 0
# DATABASE_LOCATION = '/db/users.db'
# database = Database(DATABASE_LOCATION)

@app.post('/api/log-in')
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

@app.post("/api/sign-up")
async def sign_up(request: Request):
    info = await request.json()

    username = info.get('username')
    country = info.get('country')
    email = info.get('email')
    password = info.get('password')

    print(f"username: {username}, country: {country}, email: {email}, password: {password}")

    if not (username and country and email and password):
        return Protocol.Error.invalid_request

    sign_up_success = db.sign_up(username, country, email, password)

    return {
        "success": sign_up_success
    }


@app.get("/api/practice")
def practice(request: Request, response: Response):
    client = handle_session(request, response)
    if not client.race_game:
        client.race_game = RaceGame()

    return {
        "text": client.race_game.ciphered_text
    }


@app.websocket("/api/practice")
async def receive_practice_socket(websocket: WebSocket):
    try:
        await practice_socket(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")


async def practice_socket(websocket: WebSocket):
    await websocket.accept()
    client = handle_socket_session(websocket)
    client.socket = websocket
    while client.socket:
        request = await client.socket.receive_text()
        response = handle_request(client, request)
        print("wow, response", response)
        if response:
            await client.socket.send_text(response)


def handle_request(client: Client, request: str) -> str:
    fields = Protocol.Decrypt.seperate_to_fields(request)
    if not fields:
        return Protocol.Error.empty_request

    command, *args = fields
    if command == Protocol.Command.change_letter:
        if len(args) != 2:
            return Protocol.Error.invalid_request

        from_letter, to_letter = args
        print("from", from_letter, "to", to_letter)
        client.race_game.guess_letter(from_letter, to_letter)
        response = Protocol.Encrypt.change_letter(
            client.race_game.get_gussed_count()
        )

    return response


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
