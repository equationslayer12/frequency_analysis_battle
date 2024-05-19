from fastapi import APIRouter, WebSocket, Request, Response
from starlette.websockets import WebSocketDisconnect
from protocol import Protocol
from backend.player.player import Player
from backend.text_info import TextInfo
from internals.session_utils import handle_session, handle_socket_session
import sys
sys.path.append("..")  # Adds higher directory to python modules path.


router = APIRouter()


@router.get("/api/practice")
def practice(request: Request, response: Response):
    web_client = handle_session(request, response)
    if not web_client.player:
        game = TextInfo()
        web_client.join_game(game)

    return {
        "text": web_client.text_info.ciphered_text,
        "cipheredLettersCount": web_client.text_info.ciphered_letter_count
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

    web_client = handle_socket_session(websocket)
    if not web_client:
        print("client is none... why??")
        return None

    client_player = web_client.player

    while web_client.socket:
        request = await web_client.socket.receive_text()
        response = handle_socket_request(client_player, request)
        print("wow, response", response)
        if response:
            try:
                await web_client.send_socket_response(response)
            except TypeError:
                return
            if response == Protocol.GAME_ENDED:
                print("ended...")
                web_client.leave_game()
                await web_client.close_socket()
                return


def handle_socket_request(player: Player, request: str) -> str:
    """Get response to a websocket request, and change the player's text progress.

    Args:
        player (Player): player in freq battle game
        request (str): the player request

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
        print(f"{player.username} | From {from_letter} to {to_letter}")
        player.progress.guess_letter(from_letter, to_letter)

        if player.progress.has_won():
            response = Protocol.GAME_ENDED
        else:
            response = Protocol.Encrypt.change_letter(
                player.progress.get_gussed_count()
            )

    if command == Protocol.Command.new_text:
        print("new texting....")
        player.leave_game()

        game = TextInfo()
        player.join_game(game)
        response = Protocol.GAME_ENDED

    return response
