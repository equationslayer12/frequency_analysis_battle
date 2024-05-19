from text_progress import TextProgress
from backend.text_info import TextInfo


class Player:
    """A player in a game."""

    def __init__(self, username) -> None:
        self.username = username
        self.progress: TextProgress = None
        self.game: TextInfo = None

    def join_game(self, text_info: TextInfo):
        self.race_game = text_info
        self.progress = TextProgress(text_info.decipher_dictionary)

    def leave_game(self):
        self.race_game = None
        self.progress = None
