import random
from backend.internals.encryption.aes import AESCipher
from internals.http_session import HTTPSession
from race_game import RaceGame
from fastapi import WebSocket

class Client:
    def __init__(self, session: HTTPSession) -> None:
        self.is_guest = True
        self.session: HTTPSession = session
        self.username: str = "Guest"
        self.socket: WebSocket = None
        self.AESC: AESCipher = None
        self.race_game: RaceGame = None

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
    
    async def send_response(self, message: str):
        """Send a message to the client through the client-server websocket.

        Args:
            message (str): message data

        Raises:
            TypeError: socket is closed
        """
        if self.socket:
            await self.socket.send_text(message)
        else:
            raise TypeError("Socket is closed")
        
    def end_game(self):
        self.race_game = None
    
    def start_game(self):
        self.race_game = RaceGame()

    async def close_socket(self):
        """close the client-server websocket"""
        if self.socket:
            await self.socket.close()
    