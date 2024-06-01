import asyncio
from backend.web.web_client import WebClient
from backend.text.text_info import TextInfo
from backend.config.protocol import Protocol
from typing import Dict, List
from backend.config.constants import COUNTDOWN_SECONDS, CLIENT_THRESHOLD, QUEUE, COUNTDOWN, ONGOING, ENDED, TIME_LIMIT


class WebLobby:
    """
    Represents a lobby where clients can join and play the game.
    """

    def __init__(self, lobby_id) -> None:
        """
        Initialize the WebLobby.

        Args:
            lobby_id: The unique ID of the lobby.
        """
        self.clients: Dict[int, WebClient] = {}
        self._clients_finished_count = 0
        self.text_info = TextInfo()
        self.status = QUEUE
        self._countdown_event = asyncio.Event()
        self.lobby_id = lobby_id

    async def notify_all(self, info: str, not_including=None):
        """
        Send information to all clients' sockets inside the lobby.

        Args:
            info (str): Information to send.
            not_including: A specific client to exclude from the notification.
        """
        for _, web_client in self.clients.items():
            if web_client == not_including:
                continue
            await web_client.send_socket_response(info)

    async def start_countdown(self):
        """
        Start the countdown before the game begins.
        """
        self.status = COUNTDOWN
        self._countdown_event.set()  # set countdown event to start.
        await asyncio.sleep(COUNTDOWN_SECONDS)
        self.status = ONGOING

    async def wait_for_countdown(self):
        """
        Wait for the countdown to start.
        """
        if self.status != QUEUE:
            print("no, isn't queue. started already.")
            return
        await self._countdown_event.wait()

    async def add_client(self, client: WebClient) -> bool:
        """
        Add a client to the lobby.

        Args:
            client (WebClient): The client to add.

        Returns:
            bool: True if the client was successfully added, False otherwise.
        """
        if not client or client.user_id in self.clients:
            return False
        self.clients[client.user_id] = client
        return True

    def remove_client(self, client: WebClient) -> bool:
        """
        Remove a client from the lobby.

        Args:
            client (WebClient): The client to remove.

        Returns:
            bool: True if the client was successfully removed, False otherwise.
        """
        if not client or client.user_id not in self.clients:
            return False
        del self.clients[client.user_id]
        return True

    def end_game(self):
        """End the game."""
        self.status = ENDED

    async def close(self):
        """
        Close the lobby and disconnect all clients.
        """
        self.text_info.end()
        self.text_info = None
        await self.disconnect_all_clients()
        self.clients = None

    async def disconnect_all_clients(self):
        """Disconnect all clients from the lobby."""
        for client_id, web_client in self.clients.items():
            web_client.leave_game()
            web_client.leave_game()
            await web_client.close_socket()

    def client_fished(self):
        """Increment the count of clients who have finished."""
        self._clients_finished_count += 1
        if self._clients_finished_count == len(self.clients):
            self.end_game()

    def get_status(self):
        """Get the status of the lobby."""
        return self.status

    def get_usernames(self, not_including=None) -> List[str]:
        """
        Get the usernames of all clients in the lobby.

        Args:
            not_including: A specific client to exclude from the list.

        Returns:
            List[str]: List of usernames.
        """
        return [client.username for client in self.clients.values() if client is not not_including]

    def get_user_ids(self, not_including_id=None) -> List[int]:
        """
        Get the user IDs of all clients in the lobby.

        Args:
            not_including_id: A specific user ID to exclude from the list.

        Returns:
            List[int]: List of user IDs.
        """
        return [user_id for user_id in self.clients.keys() if user_id is not not_including_id]

    def get_scores(self, not_including=None) -> List[int]:
        """
        Get the scores of all clients in the lobby.

        Args:
            not_including: A specific client to exclude from the scores list.

        Returns:
            List[int]: List of scores.
        """
        scores = []
        for client in self.clients.values():
            if client == not_including:
                continue
            if client.player.progress.has_finished():
                scores.append(Protocol.FINISHED)
            else:
                scores.append(client.player.progress.get_gussed_count())
        return scores

    def contains_user_id(self, uid: int):
        """
        Check if the lobby contains a user with the given ID.

        Args:
            uid (int): The user ID to check.

        Returns:
            bool: True if the user ID is present in the lobby, False otherwise.
        """
        return uid in self.clients
