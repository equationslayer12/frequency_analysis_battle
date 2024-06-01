import asyncio
from backend.sessions.encryption.aes import AESCipher
from backend.utils.random_utils import rand_bytes
from sessions.http_session import HTTPSession
from fastapi import WebSocket, WebSocketDisconnect
from backend.player.player import Player
from backend.text.text_info import TextInfo
from backend.config.constants import UID_LENGTH


class WebClient:
    """
    Wrapper for HTTPSession, socket, player, and encryption.
    """

    def __init__(self, session: HTTPSession) -> None:
        """
        Initialize the WebClient.

        Args:
            session (HTTPSession): The HTTP session associated with the client.
        """
        self.is_guest = True
        self.username: str = "Guest"
        self.user_id: int = self.generate_random_uid()  # per session
        self.session: HTTPSession = session
        self.socket: WebSocket = None
        self.AESC: AESCipher = None
        self.player: Player = None
        self.text_info: TextInfo = None

        self.lock = asyncio.Lock()

    def join_game(self, text_info: TextInfo):
        """
        Join a game with the provided TextInfo.

        Args:
            text_info (TextInfo): Information about the game to join.
        """
        self.text_info = text_info

        # Create a player to join the game
        self.create_player()
        # Join the game
        self.player.join_game(text_info)

    def leave_game(self):
        """Leave the current game."""
        self.player.leave_game()
        self.player = None
        self.text_info = None

    def create_player(self):
        """Create a player."""
        self.player = Player(self.username)

    def set_aes_key(self, aes_key: str):
        """
        Set the AES key for encryption.

        Args:
            aes_key (str): The AES key.
        """
        self.AESC: AESCipher = AESCipher(key=aes_key)

    def decrypt(self, encrypted_message: str):
        """
        Decrypt an encrypted message using AES.

        Args:
            encrypted_message (str): The encrypted message.

        Returns:
            str: The decrypted message.
        """
        if not self.AESC:
            print("no aesc")
            return None
        try:
            return self.AESC.decrypt(encrypted_message)
        except Exception as e:
            print(e)
            return None

    def log_in(self, username: str):
        """
        Log in the user with the provided username.

        Args:
            username (str): The username to log in with.
        """
        self.is_guest = False
        self.username = username

    def generate_random_uid(self):
        """
        Generate a random user ID.

        Returns:
            int: The generated user ID.
        """
        return rand_bytes(UID_LENGTH)

    async def send_socket_response(self, message: str):
        """
        Send a message to the client through the WebSocket.

        Args:
            message (str): The message to send.

        Raises:
            WebSocketDisconnect: If the socket is closed.
        """
        async with self.lock:
            if self.socket:
                await self.socket.send_text(message)
            else:
                raise WebSocketDisconnect

    async def receive_socket_request(self) -> str:
        """
        Receive a message from the client through the WebSocket.

        Returns:
            str: The received message.

        Raises:
            WebSocketDisconnect: If the socket is closed.
        """
        async with self.lock:
            if self.socket:
                return await self.socket.receive_text()
            else:
                raise WebSocketDisconnect

    async def close_socket(self):
        """Close the WebSocket connection."""
        if self.socket:
            await self.socket.close()
