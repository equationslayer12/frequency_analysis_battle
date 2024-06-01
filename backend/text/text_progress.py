from backend.config.protocol import Protocol


class TextProgress:
    """
    Represents the progress of the client in guessing the ciphered text.
    Tracks which letters have been guessed and how many of them are correct.
    """

    def __init__(self, decipher_dictionary: dict) -> None:
        """
        Initialize the TextProgress with the decipher dictionary.

        Args:
            decipher_dictionary (dict): A dictionary mapping ciphered letters to their original counterparts.
        """
        self.guessed = {}
        self.guessed_correctly = 0

        self.decipher_dictionary = decipher_dictionary
        self.chipered_letter_count = len(decipher_dictionary)
        # user has to change chipered_letter_count letters to win

    def get_guessed_count(self) -> int:
        """
        Get the count of guessed letters.

        Returns:
            int: The count of guessed letters.
        """
        return len(self.guessed)

    def guess_letter(self, from_letter: str, to_letter: str):
        """
        Process a letter guess made by the user.

        Args:
            from_letter (str): The original letter.
            to_letter (str): The guessed letter.
        """
        if from_letter is None or to_letter is None:
            return

        # If the changed letter isn't in the ciphered text
        if self.decipher_dictionary.get(from_letter) is None:
            return

        already_guessed_letter = self.guessed.get(from_letter)
        if already_guessed_letter:
            # If nothing changed
            if to_letter == already_guessed_letter:
                return

            # If the previous letter was correct
            if self.check_guess(from_letter, already_guessed_letter):
                self.guessed_correctly -= 1

            # If a letter was deleted
            if to_letter == Protocol.DELETE_CHAR:
                print(f"Deleting dict[{from_letter}]: {self.guessed[from_letter]}")
                del self.guessed[from_letter]
                return

        # If trying to delete, but nothing was guessed earlier
        elif to_letter == Protocol.DELETE_CHAR:
            return

        self.guessed[from_letter] = to_letter
        is_correct_letter = self.check_guess(from_letter, to_letter)
        if is_correct_letter:
            self.guessed_correctly += 1
        print(f"{self.guessed_correctly} / {self.chipered_letter_count}")

    def check_guess(self, from_letter: str, to_letter: str) -> bool:
        """
        Check if a letter guess is correct.

        Args:
            from_letter (str): The original letter.
            to_letter (str): The guessed letter.

        Returns:
            bool: True if the guessed letter is correct, False otherwise.
        """
        real_letter = self.decipher_dictionary.get(from_letter)
        if real_letter is None:
            return False

        return real_letter == to_letter

    def has_finished(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.guessed_correctly == self.chipered_letter_count
