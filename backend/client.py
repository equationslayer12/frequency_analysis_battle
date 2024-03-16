import random
from session import Session

class Client:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.nickname = random.randint(100, 1000000)
        self.socket = None
        self.race_game = None
    