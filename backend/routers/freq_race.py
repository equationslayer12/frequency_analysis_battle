import asyncio
import time
from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect
from backend.constants import COUNTDOWN, ONGOING, QUEUE
from internals.session_utils import handle_session, handle_socket_session
from protocol import Protocol
from web_client import WebClient
from web_lobby import WebLobby
from backend.text_info import TextInfo
from typing import List

router = APIRouter()

queuing_lobbies: List[WebLobby] = []
ongoing_lobbies: List[WebLobby] = []


def find_a_lobby_for_client(web_client: WebClient) -> TextInfo:
    """Search for games in queuing_games, if empty create one.
    Args:
        client (Client): the client that wants to join a game.
    Returns:
        Game: matched game for client.
    """
    if len(queuing_lobbies) == 0:
        new_lobby = WebLobby()
        queuing_lobbies.append(new_lobby)

    lobby = queuing_lobbies[-1]
    return lobby


@router.websocket("/api/race/join")
async def join_race_game_endpoint(websocket: WebSocket):
    print("client joining..")
    try:
        await join_race_game(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
        return Protocol.Error.invalid_request


async def join_race_game(websocket: WebSocket):
    await websocket.accept()

    web_client = handle_socket_session(websocket)
    if not web_client:
        print("client is none... why??")
        return None

    lobby: WebLobby = find_a_lobby_for_client(web_client)

    text_info: TextInfo = lobby.text_info
    text_length_response = Protocol.Encrypt.text_length(
        text_info.ciphered_letter_count)
    await web_client.send_socket_response(text_length_response)

    ack = await web_client.receive_socket_request()

    opponents = lobby.get_usernames(not_including=web_client)
    await web_client.send_socket_response(Protocol.Encrypt.opponents(opponents))

    print(lobby.clients)
    if not lobby.contains_user_id(web_client.user_id):
        info = Protocol.Encrypt.Event.player_joined(web_client.username)
        await lobby.notify_all(info)

        await lobby.add_client(web_client)  # may trigger countdown

    else:
        ...  # already connected

    print(
        f"paired client {web_client.username} with text:\n{lobby.text_info.ciphered_text}")

    web_client.join_game(text_info)
    # print(f"game now contains {len(lobby.clients)} clients: {lobby.clients}")

    if 0:
        try:
            for i in range(100):
                await web_client.send_socket_response("heartbeat")
                await asyncio.sleep(3)
        except Exception as e:
            print(e)
            print("DONE! QUITTING!!!!!!!!!!!!!!!!!!!")

    print(web_client.username, "is logged in:", not web_client.is_guest)

    print("waiting until countdown starts")
    await lobby.wait_for_countdown()
    await client_racing(lobby, web_client)


async def client_racing(lobby: WebLobby, client: WebClient):
    """Client joined a race game against other players. this function handles the socket

    Args:
        client (WebClient): client
    """
    # send initial information: usernames.
    # equationslayer12 donde pablo
    text_info = lobby.text_info
    print("started a race for:", client.socket)
    print(lobby.status)
    while lobby.status == ONGOING or lobby.status == COUNTDOWN:
        print("clienting asking...")
        request = await client.receive_socket_request()
        print(client.username, "asked for", request)
        if request == Protocol.Request.text:
            await client.send_socket_response(text_info.ciphered_text)
