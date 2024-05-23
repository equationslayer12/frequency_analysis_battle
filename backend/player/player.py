from text_progress import TextProgress
from backend.text_info import TextInfo


class Player:
    """A player in a game."""

    def __init__(self, username) -> None:
        self.username = username
        self.progress: TextProgress = None
        self.text_info: TextInfo = None
        self.is_finished = False

    def join_game(self, text_info: TextInfo):
        self.text_info = text_info
        self.progress = TextProgress(text_info.decipher_dictionary)
        self.is_finished = self.progress.has_finished()

    def finish_game(self):
        self.is_finished = True

    def leave_game(self):
        self.text_info = None
        self.progress = None
