from text_handler import TextHandler
from user.user import User
from typing import Dict


text_handler = TextHandler()


class RaceGame:
    def __init__(self) -> None:
        self.is_ongoing = False
        self.users: Dict[str: User] = {}  # from username to user class

        self.real_text = text_handler.get_random_text()

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.decipher_dictionary = cipheredObject.decipher_dictionary
        self.chipered_letter_count = len(self.decipher_dictionary)
        # user has to change chipered_letter_count letters to win

    def add_user(self, user: User) -> bool:
        if not user:
            return False
        if user.username in self.users:
            return False

        self.users[user.username] = user
        return True

    def remove_players(self, user: User) -> bool:
        if not user:
            return False
        if user.username not in self.users:
            return False

        del self.users[user.username]
        return True

    def start(self):
        self.is_ongoing = True

    def end(self):
        self.is_ongoing = False

    def get_usernames(self):
        return self.users.keys()
