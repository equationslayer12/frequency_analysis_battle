import re

def is_letter(letter: str) -> bool:
    """
    Check if a character is an alphabet letter.

    Args:
        letter (str): The character to be checked.

    Returns:
        bool: True if the character is an alphabet letter, False otherwise.
    """
    return re.match("^[a-zA-Z]$", letter) is not None

if __name__ == "__main__":
    print(is_letter('A'))  # Output: True
