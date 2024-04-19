from fastapi import APIRouter, WebSocket, Request, Response
from starlette.websockets import WebSocketDisconnect
from protocol import Protocol
from client import Client
from race_game import RaceGame
from internals.session_utils import handle_session, handle_socket_session
import sys
sys.path.append("..")  # Adds higher directory to python modules path.


router = APIRouter()


@router.get("/api/practice")
def practice(request: Request, response: Response):
    client = handle_session(request, response)
    if not client.race_game:
        client.start_game()

    return {
        "text": client.race_game.ciphered_text,
        "cipheredLettersCount": client.race_game.chipered_letter_count
    }


@router.websocket("/api/practice")
async def receive_practice_socket(websocket: WebSocket):
    try:
        await practice_socket(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
        return Protocol.Error.invalid_request


async def practice_socket(websocket: WebSocket):
    await websocket.accept()

    client = handle_socket_session(websocket)
    if not client:
        print("client is none... why??")
        return None
    client.socket = websocket
    while client.socket:
        request = await client.socket.receive_text()
        response = handle_socket_request(client, request)
        print("wow, response", response)
        if response:
            try:
                await client.send_response(response)
            except TypeError:
                return
            if response == Protocol.GAME_ENDED:
                print("ended...")
                client.end_game()
                client.close_socket()
                return



def handle_socket_request(client: Client, request: str) -> str:
    """Get response to a websocket request.
    Side effects:
        may change letters in client.race_game
        may end client.race_game

    Args:
        client (Client): client in freq battle game
        request (str): the client request

    Returns:
        str: response
    """
    fields = Protocol.Decrypt.seperate_to_fields(request)
    if not fields:
        return Protocol.Error.empty_request

    command, *args = fields
    if command == Protocol.Command.change_letter:
        if len(args) != 2:
            return Protocol.Error.invalid_request

        from_letter, to_letter = args
        print(f"{client.username} | From {from_letter} to {to_letter}")
        client.race_game.guess_letter(from_letter, to_letter)

        if client.race_game.has_won():
            response = Protocol.GAME_ENDED
        else:
            response = Protocol.Encrypt.change_letter(
                client.race_game.get_gussed_count()
            )

    if command == Protocol.Command.new_text:
        print("new texting....")
        client.end_game()
        client.start_game()
        response = Protocol.GAME_ENDED

    return response
