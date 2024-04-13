from internals.session_utils import handle_session, handle_socket_session
from race_game import RaceGame
from client import Client
from protocol import Protocol
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket, Request, Response
import sys
sys.path.append("..")  # Adds higher directory to python modules path.


router = APIRouter()


@router.get("/api/practice")
def practice(request: Request, response: Response):
    client = handle_session(request, response)
    if not client.race_game:
        client.race_game = RaceGame()

    return {
        "text": client.race_game.ciphered_text
    }


@router.websocket("/api/practice")
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
            try:
                await client.send_response(response)
            except TypeError:
                return
        
        if response == Protocol.GAME_ENDED:
            client.close_socket()


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
