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

    matched_game = queuing_games[-1]
    return matched_game


@router.websocket("/api/race/join")
async def join_race_game(websocket: WebSocket):
    try:
        await websocket.accept()
        web_client = handle_socket_session(websocket)
        game = find_a_game_for_client(web_client)
        connected_usernames = game.get_usernames()
        print(f"paired client {web_client.username} with text:\n{game.ciphered_text}")
        if game:
            web_client.join_game(game)
            print(f"game now contains {len(game.users)} users: {game.users}")
            await client_racing(web_client, connected_usernames)

            print(web_client.username, "is logged in:", not web_client.is_guest)

    except WebSocketDisconnect:
        print("Client disconnected")
        web_client.leave_game()
        return Protocol.Error.invalid_request


async def client_racing(client: WebClient, opponents):
    """Client joined a race game against other players. this function handles the socket

    Args:
        client (WebClient): client
    """
    # send initial information: usernames.
    # equationslayer12 donde pablo
    print("clienting socketing:", client.socket)
    await client.send_response("hi")

