from backend.text.text_handler import TextHandler


text_handler = TextHandler()


class TextInfo:
    def __init__(self) -> None:
        self.is_ongoing = False

        self.real_text = text_handler.get_random_text()

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.decipher_dictionary = cipheredObject.decipher_dictionary
        self.ciphered_letter_count = len(self.decipher_dictionary)
        # user has to change chipered_letter_count letters to win

    def start(self):
        self.is_ongoing = True

    def end(self):
        self.is_ongoing = False
