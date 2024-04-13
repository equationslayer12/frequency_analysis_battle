import random
from internals.http_session import HTTPSession
from race_game import RaceGame


class Client:
    def __init__(self, session: HTTPSession) -> None:
        self.session = session
        self.nickname = random.randint(100, 1000000)
        self.socket = None
        self.race_game: RaceGame = None

    def send_response(self, message: str):
        """Send a message to the client through the client-server websocket.

        Args:
            message (str): message data

        Raises:
            TypeError: socket is closed
        """
        if self.socket:
            self.socket.send_text(message)
        else:
            raise TypeError("Socket is closed")

    def close_socket(self):
        """close the client-server websocket"""
        if self.socket:
            self.socket.close()