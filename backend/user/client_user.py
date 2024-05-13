from .user import User
from race_game import RaceGame
from text_progress import TextProgress


class ClientUser(User):
    """The player in a game."""
    def __init__(self, username):
        super().__init__(username)

    def join_game(self, game: RaceGame):
        self.race_game = game
        self.progress = TextProgress(game.decipher_dictionary)

    def leave_game(self):
        self.race_game = None
        self.progress = None

