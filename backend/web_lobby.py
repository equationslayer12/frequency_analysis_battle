import asyncio
from web_client import WebClient
from text_info import TextInfo
from protocol import Protocol
from typing import Dict, List
from constants import COUNTDOWN_SECONDS, CLIENT_THRESHOLD, QUEUE, COUNTDOWN, ONGOING, ENDED, TIME_LIMIT


class WebLobby:
    def __init__(self, lobby_id) -> None:
        self.clients: Dict[int, WebClient] = {}
        self._clients_finished_count = 0
        self.text_info = TextInfo()
        self.status = QUEUE
        self._countdown_event = asyncio.Event()
        self.lobby_id = lobby_id

    async def notify_all(self, info: str, not_including=None):
        """send information to all clients' sockets inside the lobby

        Args:
            info (str): information to send
        """

        # TODO: Convert to threads.
        threads = []
        for _, web_client in self.clients.items():
            if web_client == not_including:
                continue
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
        return True

    def remove_client(self, client: WebClient) -> bool:
        if not client:
            return False
        if client.user_id not in self.clients:
            return False

        del self.clients[client.user_id]
        return True

    def end_game(self):
        self.status = ENDED
    
    async def close(self):
        self.text_info.end()
        self.text_info = None
        await self.disconnect_all_clients()

        self.clients = None

    async def disconnect_all_clients(self):
        for client_id, web_client in self.clients.items():
            web_client.leave_game()
            web_client.leave_game()
            await web_client.close_socket()

    def client_fished(self):
        self._clients_finished_count += 1
        if self._clients_finished_count == len(self.clients):
            self.end_game()

    def get_status(self):
        return self.status

    def get_usernames(self, not_including=None) -> List[str]:
        """get lobby's players' usernames

        Args:
            not_including (WebClient, optional): a specific client to not include in the scores list. Defaults to None.

        Returns:
            List[str]: list of usernames
        """
        return [client.username for client in self.clients.values() if client is not not_including]

    def get_user_ids(self, not_including_id=None) -> List[int]:
        """get lobby's players' ids.

        Args:
            not_including_id (int, optional): a specific client id to not include in the ids list. Defaults to None.

        Returns:
            List[int]: list of ids.
        """
        return [user_id for user_id in self.clients.keys() if user_id is not not_including_id]

    def get_scores(self, not_including=None) -> List[int]:
        """get lobby's players' scores. if finished, the score will be protocol.FINISHED.

        Args:
            not_including (WebClient, optional): a specific client to not include in the scores list. Defaults to None.

        Returns:
            List[int]: players' scores.
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
        return uid in self.clients
