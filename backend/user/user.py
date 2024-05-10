from text_progress import TextProgress

class User:
    """A player in a game."""
    def __init__(self, username) -> None:
        self.username = username
        self.progress: TextProgress = None

