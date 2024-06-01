from backend.utils.random_utils import rand_bytes
from backend.config.protocol import Protocol
import asyncio
from typing import Dict
from backend.config.constants import CLIENT_THRESHOLD, LOBBYID_LENGTH, TIME_LIMIT
from backend.text.text_info import TextInfo
from backend.web.web_client import WebClient
from backend.web.web_lobby import WebLobby


class LobbyHandler:
    """
    Manages the creation and handling of lobbies for a web application.
    """

    def __init__(self) -> None:
        """
        Initializes the LobbyHandler with empty dictionaries for queuing and ongoing lobbies.
        """
        self.queuing_lobbies: Dict[int, WebLobby] = {}
        self.ongoing_lobbies: Dict[int, WebLobby] = {}

    def find_lobby_for_client(self, web_client: WebClient) -> TextInfo:
        """Search for games in queuing_games, if empty create one.
        Args:
            client (Client): the client that wants to join a game.
        Returns:
            Game: matched game for client.
        """
        if len(self.queuing_lobbies) == 0:
            new_lobby = WebLobby(self.generate_lobby_id())
            self.queuing_lobbies[new_lobby.lobby_id] = new_lobby

        lobby = next(iter(self.queuing_lobbies.values()))
        return lobby

    async def add_client(self, lobby: WebLobby, web_client: WebLobby):
        """Adds a client to the lobby. Might trigger countdown before game starts. 

        Args:
            lobby (WebLobby): the web lobby
            web_client (WebLobby): web client
        """
        added = await lobby.add_client(web_client)
        if not added:
            return
        
        should_start_countdown = len(lobby.clients) >= CLIENT_THRESHOLD
        print("should start:", should_start_countdown)
        if should_start_countdown:
            del self.queuing_lobbies[lobby.lobby_id]
            self.ongoing_lobbies[lobby.lobby_id] = lobby

            await lobby.notify_all(Protocol.Encrypt.Event.START_COUNTDOWN)
            await lobby.start_countdown()

        self.time_limit(lobby)

    async def time_limit(self, lobby: WebLobby):
        asyncio.sleep(TIME_LIMIT)
        lobby.end_game()
        await lobby.close()
        print("ended...")
        
        del self.ongoing_lobbies[lobby.lobby_id]


    def generate_lobby_id(self):
        new_lobby_id = rand_bytes(LOBBYID_LENGTH)
        while new_lobby_id in self.queuing_lobbies or new_lobby_id in self.ongoing_lobbies:
            new_lobby_id = rand_bytes(LOBBYID_LENGTH)

        return new_lobby_id
