import json
import sys
from pathlib import Path

# Adds the parent directory to the Python module search path
sys.path.append("..")

try:
    from backend.config.constants import TEXTS_PATH
except ModuleNotFoundError:
    print("Don't forget to `cd backend`")
    sys.exit(1)


def add_text_to_json(file_path: str, new_text: str) -> None:
    """
    Add a new text to a JSON file containing a list of texts.

    Args:
        file_path (str): The path to the JSON file.
        new_text (str): The new text to be added.
    """
    # Read the existing JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    # Add the new text
    data["texts"].append(new_text)

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

    print(f'Text added successfully:\n\n{new_text}\n')


def main() -> None:
    """
    Main function to add a new text to the JSON file.
    """
    # Sample text to be added
    TEXT = """
    This runway is covered with the last pollen from the last flowers available anywhere on Earth.
    That means this is our Last Chance. We're the only ones who make honey, pollinate flowers and dress like this.
    If we're gonna survive as a species, this is our moment! What do you say?
    Are we going to be bees, or just Museum of Natural History keychains?
    We're bees!
    Keychain!
    Then follow me! Except Keychain.
    """

    # Clean and format the text
    clean_text = TEXT.strip().upper().replace("\n", " ")

    # Add the text to the JSON file
    add_text_to_json(TEXTS_PATH, clean_text)


if __name__ == "__main__":
    main()
