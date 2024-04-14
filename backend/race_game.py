from text_handler import TextHandler
from protocol import Protocol

text_handler = TextHandler()


class RaceGame:
    def __init__(self) -> None:
        self.real_text = text_handler.get_random_text()

        self.guessed = {}
        self.guessed_correctly = 0

        cipheredObject = text_handler.cipher_text(self.real_text)
        self.ciphered_text = cipheredObject.text
        self.decipher_dictionary = cipheredObject.decipher_dictionary
        # user has to change chipered_letter_count letters to win
        self.chipered_letter_count = len(self.decipher_dictionary)

    def get_gussed_count(self) -> int:
        return len(self.guessed)

    def guess_letter(self, from_letter: str, to_letter: str):
        """User changed a letter to another.

        Args:
            from_letter (str): the original letter
            to_letter (str): guessed letter
        """
        if from_letter is None or to_letter is None:
            return

        # if changed letter that isn't in the ciphered text
        if self.decipher_dictionary.get(from_letter) is None:
            return

        already_gussed_letter = self.guessed.get(from_letter)
        if already_gussed_letter:
            # if nothing changed
            if to_letter == already_gussed_letter:
                return

            # if previous letter was correct
            if self.check_guess(from_letter, already_gussed_letter):
                self.guessed_correctly -= 1

            # if letter deleted
            if to_letter == Protocol.DELETE_CHAR:
                print(
                    f"deleting dict[{from_letter}] : {self.guessed[from_letter]}")
                del self.guessed[from_letter]
                return
        # if tried to delete, but nothing was guessed earlier.
        elif to_letter == Protocol.DELETE_CHAR:
            return

        self.guessed[from_letter] = to_letter
        is_correct_letter = self.check_guess(from_letter, to_letter)
        if is_correct_letter:
            self.guessed_correctly += 1
        print(f"{self.guessed_correctly} / {self.chipered_letter_count}")

    def check_guess(self, from_letter, to_letter):
        real_letter = self.decipher_dictionary.get(from_letter)
        if real_letter is None:
            return False

        return real_letter == to_letter

    def has_won(self) -> bool:
        """is the game over

        Returns:
            bool: is the game over
        """
        return self.guessed_correctly == self.chipered_letter_count
