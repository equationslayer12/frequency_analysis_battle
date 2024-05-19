import asyncio
from backend.internals.encryption.aes import AESCipher
import random
from internals.http_session import HTTPSession
from fastapi import WebSocket, WebSocketDisconnect
from backend.player.player import Player
from backend.text_info import TextInfo
from constants import UID_LENGTH


class WebClient:
    def __init__(self, session: HTTPSession) -> None:
        self.is_guest = True
        self.username: str = "Guest"
        self.user_id: int = self.generate_random_uid()  # per sesion
        self.session: HTTPSession = session
        self.socket: WebSocket = None
        self.AESC: AESCipher = None
        self.player: Player = None
        self.text_info: TextInfo = None

        self.lock = asyncio.Lock()

    def join_game(self, text_info: TextInfo):
        self.text_info = text_info

        # Create a user (a player in a game)
        self.create_player()
        # Join it
        self.player.join_game(text_info)

    def leave_game(self):
        self.player.leave_game()
        self.player = None
        self.text_info = None

    def create_player(self):
        """Create a user to join a game.
        """
        self.player = Player(self.username)

    def set_aes_key(self, aes_key: str):
        self.AESC: AESCipher = AESCipher(key=aes_key)

    def decrypt(self, encrypted_message: str):
        if not self.AESC:
            print("no aesc")
            return None
        try:
            return self.AESC.decrypt(encrypted_message)
        except Exception as e:
            print(e)
            return None

    def log_in(self, username: str):
        self.is_guest = False
        self.username = username

    def generate_random_uid(self):
        return int.from_bytes(random.randbytes(UID_LENGTH), byteorder='little')

    async def send_socket_response(self, message: str):
        """Send a message to the client through the client-server websocket.

        Args:
            message (str): message data

        Raises:
            TypeError: socket is closed
        """
        async with self.lock:
            if self.socket:
                await self.socket.send_text(message)
            else:
                raise WebSocketDisconnect

    async def receive_socket_request(self) -> str:
        async with self.lock:
            if self.socket:
                return await self.socket.receive_text()
            else:
                raise WebSocketDisconnect

    async def close_socket(self):
        """close the client-server websocket"""
        if self.socket:
            await self.socket.close()
