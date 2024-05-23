from backend.config.protocol import Protocol


class TextProgress:
    """
    Client text progress. tracks which letters have been guessed, and how many of them are correct.
    """

    def __init__(self, decipher_dictionary: dict) -> None:
        self.guessed = {}
        self.guessed_correctly = 0

        self.decipher_dictionary = decipher_dictionary
        self.chipered_letter_count = len(decipher_dictionary)
        # user has to change chipered_letter_count letters to win

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

    def check_guess(self, from_letter: str, to_letter: str):
        """check if a letter is correct

        Args:
            from_letter (str): from letter
            to_letter (str): to letter

        Returns:
            bool: is the letter correct.
        """
        real_letter = self.decipher_dictionary.get(from_letter)
        if real_letter is None:
            return False

        return real_letter == to_letter
    
    def has_finished(self) -> bool:
        """is the game over

        Returns:
            bool: is the game over
        """
        return self.guessed_correctly == self.chipered_letter_count
