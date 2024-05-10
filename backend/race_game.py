from text_handler import TextHandler
from user.user import User


text_handler = TextHandler()


class RaceGame:
    def __init__(self) -> None:
        self.is_ongoing = False
        self.users = []

        self.real_text = text_handler.get_random_text()

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.decipher_dictionary = cipheredObject.decipher_dictionary
        self.chipered_letter_count = len(self.decipher_dictionary)
        # user has to change chipered_letter_count letters to win

    def add_user(self, user: User):
        self.users.append(user)

    def start(self):
        self.is_ongoing = True

    def end(self):
        self.is_ongoing = False
