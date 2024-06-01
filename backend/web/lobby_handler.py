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
        """
        Search for an available lobby for a client. If none exists, create a new one.

        Args:
            web_client (WebClient): The client wanting to join a lobby.

        Returns:
            TextInfo: The information about the lobby found or created.
        """
        if len(self.queuing_lobbies) == 0:
            new_lobby = WebLobby(self.generate_lobby_id())
            self.queuing_lobbies[new_lobby.lobby_id] = new_lobby

        lobby = next(iter(self.queuing_lobbies.values()))
        return lobby

    async def add_client(self, lobby: WebLobby, web_client: WebClient):
        """
        Add a client to the specified lobby. Start a countdown if enough clients are present.

        Args:
            lobby (WebLobby): The lobby to add the client to.
            web_client (WebClient): The client to add.
        """
        added = await lobby.add_client(web_client)
        if not added:
            return

        should_start_countdown = len(lobby.clients) >= CLIENT_THRESHOLD
        if should_start_countdown:
            del self.queuing_lobbies[lobby.lobby_id]
            self.ongoing_lobbies[lobby.lobby_id] = lobby

            await lobby.notify_all(Protocol.Encrypt.Event.START_COUNTDOWN)
            await lobby.start_countdown()

        await self.time_limit(lobby)

    async def time_limit(self, lobby: WebLobby):
        """
        Apply a time limit to the lobby's game session. End the game after the time limit.

        Args:
            lobby (WebLobby): The lobby to apply the time limit to.
        """
        await asyncio.sleep(TIME_LIMIT)
        lobby.end_game()
        await lobby.close()
        del self.ongoing_lobbies[lobby.lobby_id]

    def generate_lobby_id(self):
        """
        Generate a unique lobby ID.

        Returns:
            int: A unique lobby ID.
        """
        new_lobby_id = rand_bytes(LOBBYID_LENGTH)
        while new_lobby_id in self.queuing_lobbies or new_lobby_id in self.ongoing_lobbies:
            new_lobby_id = rand_bytes(LOBBYID_LENGTH)

        return new_lobby_id
