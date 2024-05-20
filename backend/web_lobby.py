import asyncio
import threading
import time
from web_client import WebClient
from text_info import TextInfo
from protocol import Protocol
from typing import Dict
from constants import COUNTDOWN_SECONDS, CLIENT_THRESHOLD, QUEUE, COUNTDOWN, ONGOING, ENDED


class WebLobby:
    def __init__(self) -> None:
        self.clients: Dict[int, WebClient] = {}
        self.text_info = TextInfo()
        self.status = QUEUE
        self._countdown_event = asyncio.Event()

    async def notify_all(self, info: str):
        """send information to all clients' sockets inside the lobby

        Args:
            info (str): information to send
        """

        # TODO: Convert to threads.
        threads = []
        for _, web_client in self.clients.items():
            await web_client.send_socket_response(info)

    async def start_countdown(self):
        """Sets self.status to countdown, sleeps, then selts. self.status to ongoing.

        Returns:
            Promise: a promise to the countdown
        """
        print("-=-=- its the final countdown -=-=-")
        self.status = COUNTDOWN

        self._countdown_event.set()  # set countdown event to start.

        await asyncio.sleep(COUNTDOWN_SECONDS)
        self.status = ONGOING

    async def wait_for_countdown(self):
        if self.status != QUEUE:
            print("no, isn't queue. started already.")
            return

        await self._countdown_event.wait()

    async def add_client(self, client: WebClient) -> bool:
        """Adds a client to the lobby.
        Might trigger countdown before game starts.

        Args:
            client (WebClient): client

        Returns:
            bool: success
        """
        if not client:
            return False
        if client.user_id in self.clients:
            return False

        self.clients[client.user_id] = client

        should_start_countdown = len(self.clients) >= CLIENT_THRESHOLD
        print("should start:", should_start_countdown)
        if should_start_countdown:
            await self.notify_all(Protocol.Encrypt.Event.START_COUNTDOWN)
            await self.start_countdown()

        return True

    def remove_client(self, client: WebClient) -> bool:
        if not client:
            return False
        if client.user_id not in self.clients:
            return False

        del self.clients[client.user_id]
        return True

    def get_usernames(self, not_including=None):
        return [client.username for client in self.clients.values() if client is not not_including]

    def contains_user_id(self, uid: int):
        return uid in self.clients
