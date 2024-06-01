from backend.text.text_handler import TextHandler

text_handler = TextHandler()

class TextInfo:
    """
    A class to manage information about the text game.

    Attributes:
        is_ongoing (bool): Indicates if the game is ongoing.
        real_text (str): The original text.
        ciphered_text (str): The ciphered text.
        decipher_dictionary (dict): A dictionary to map ciphered letters back to original letters.
        ciphered_letter_count (int): The number of unique ciphered letters in the text.
    """
    def __init__(self) -> None:
        """
        Initialize the TextInfo with random text and cipher it.
        """
        self.is_ongoing = False

        self.real_text = text_handler.get_random_text()

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.decipher_dictionary = cipheredObject.decipher_dictionary
        self.ciphered_letter_count = len(self.decipher_dictionary)
        # user has to change chipered_letter_count letters to win

    def start(self):
        """
        Start the text game.
        """
        self.is_ongoing = True

    def end(self):
        """
        End the text game.
        """
        self.is_ongoing = False
