import asyncio
import time
from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect
from backend.constants import COUNTDOWN, ENDED, ONGOING, QUEUE
from backend.player.player import Player
from internals.session_utils import handle_session, handle_socket_session
from protocol import Protocol
from web_client import WebClient
from web_lobby import WebLobby
from backend.text_info import TextInfo
from typing import List
from lobby_handler import LobbyHandler

router = APIRouter()

lobby_handler = LobbyHandler()




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

    lobby: WebLobby = lobby_handler.find_lobby_for_client(web_client)

    text_info: TextInfo = lobby.text_info
    text_length_response = Protocol.Encrypt.text_length(
        text_info.ciphered_letter_count)
    await web_client.send_socket_response(text_length_response)

    ack = await web_client.receive_socket_request()

    opponents_usernames = lobby.get_usernames(not_including=web_client)
    opponents_user_ids = lobby.get_user_ids(
        not_including_id=web_client.user_id)
    await web_client.send_socket_response(Protocol.Encrypt.opponents(opponents_usernames, opponents_user_ids))

    print(lobby.clients)
    if not lobby.contains_user_id(web_client.user_id):
        info = Protocol.Encrypt.Event.player_joined(
            web_client.username, web_client.user_id)
        await lobby.notify_all(info)

        await lobby_handler.add_client(lobby, web_client)

    else:
        ...  # already connected

    print(
        f"paired client {web_client.username} with text:\n{lobby.text_info.ciphered_text}"
    )

    web_client.join_game(text_info)
    # print(f"game now contains {len(lobby.clients)} clients: {lobby.clients}")

    print(web_client.username, "is logged in:", not web_client.is_guest)

    print("waiting until countdown starts")
    await lobby.wait_for_countdown()
    await client_racing(lobby, web_client)


async def client_racing(lobby: WebLobby, web_client: WebClient):
    """Client joined a race game against other players. this function handles the socket

    Args:
        client (WebClient): client
    """
    # send initial information: usernames.
    # equationslayer12 donde pablo
    text_info = lobby.text_info
    print("started a race for:", web_client.socket)
    print(lobby.status)
    while lobby.status in (COUNTDOWN, ONGOING, ENDED):
        print("clienting asking...")
        request = await web_client.receive_socket_request()
        print(web_client.username, "asked for", request)

        response = handle_socket_request(lobby, web_client, request)
        print("wow, response", response)
        if response:
            try:
                await web_client.send_socket_response(response)
            except TypeError:
                return
            if response == str(Protocol.FINISHED):
                print("Oh slap! He finished!")
                web_client.player.finish_game()
                lobby.client_fished()


def handle_socket_request(lobby: WebLobby, web_client: WebClient, request: str) -> str:
    """Get response to a websocket request, and change the player's text progress.

    Args:
        web_client (WebClient): client in freq battle game
        request (str): the player request

    Returns:
        str: response
    """

    if request == Protocol.Request.text:
        return web_client.text_info.ciphered_text

    fields = Protocol.Decrypt.seperate_to_fields(request)
    if not fields:
        return Protocol.Error.empty_request

    response = None
    command, *args = fields
    if command == Protocol.Command.change_letter:
        player = web_client.player

        if len(args) != 2 or player.is_finished:
            return Protocol.Error.invalid_request

        from_letter, to_letter = args
        print(f"{player.username} | From {from_letter} to {to_letter}")
        player.progress.guess_letter(from_letter, to_letter)
        if player.progress.has_finished():
            response = Protocol.Encrypt.finished()
        else:
            response = Protocol.Encrypt.change_letter(
                player.progress.get_gussed_count()
            )
    if command == Protocol.Request.sync:
        user_ids = lobby.get_user_ids(not_including_id=web_client.user_id)
        scores = lobby.get_scores(not_including=web_client)
        game_status = lobby.get_status()
        response = Protocol.Encrypt.sync(user_ids, scores, game_status)

    return response
