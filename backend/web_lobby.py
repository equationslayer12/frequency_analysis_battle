import asyncio
import threading
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
        print("its the final countdown")
        self.status = COUNTDOWN
        await self.notify_all(Protocol.Encrypt.Event.START_COUNTDOWN)
        await asyncio.sleep(COUNTDOWN_SECONDS)
        self.status = ONGOING

    async def add_client(self, client: WebClient) -> bool:
        if not client:
            return False
        if client.user_id in self.clients:
            return False

        info = Protocol.Encrypt.Event.player_joined(client.username)
        await self.notify_all(info)

        self.clients[client.user_id] = client

        if len(self.clients) >= CLIENT_THRESHOLD:
            print("its is!!")
            thread = threading.Thread(target=asyncio.run, args=(self.start_countdown()))
            thread.start()

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
