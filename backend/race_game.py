from text_handler import TextHandler

text_handler = TextHandler()
class RaceGame:
    def __init__(self) -> None:
        self.real_text = text_handler.get_random_text()

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.dictionary = cipheredObject.dictionary
    