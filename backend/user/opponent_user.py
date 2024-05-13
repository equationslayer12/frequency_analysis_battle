from user import User

class OpponentUser(User):
    """An opponent player in a game"""
    def __init__(self, username):
        super().__init__(username)
