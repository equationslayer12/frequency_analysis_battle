from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from internals.session_utils import handle_session, handle_socket_session
from protocol import Protocol
from web_client import WebClient
from race_game import RaceGame

router = APIRouter()

queuing_games = []
ongoing_games = []


def find_a_game_for_client(web_client: WebClient) -> RaceGame:
    """Search for games in queuing_games, if empty create one.
    Args:
        client (Client): the client that wants to join a game.
    Returns:
        Game: matched game for client.
    """
    matched_game = None
    if len(queuing_games) == 0:
        new_game = RaceGame()
        queuing_games.append(new_game)

    return matched_game[-1]


@router.websocket("/api/race/join")
async def join_race_game(websocket: WebSocket):
    try:
        await websocket.accept()
        client = handle_socket_session(websocket)
        game = find_a_game_for_client(client)
        if game:
            client.start_game(game)
            game.add_player(client)
            await client_racing(client)

            print(client.username, "is guest:", client.is_guest)

    except WebSocketDisconnect:
        print("Client disconnected")
        return Protocol.Error.invalid_request


async def client_racing(client: WebClient):
    ...
