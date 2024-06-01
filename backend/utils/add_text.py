import json
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
try:
    from backend.config.constants import TEXTS_PATH

except ModuleNotFoundError:
    print("dont forget to `cd backend`")
    sys.exit(1)

TEXT = """
This runway is covered with the last pollen from the last flowers available anywhere on Earth.
That means this is our Last Chance. We're the only ones who make honey, pollinate flowers and dress like this.
If we're gonna survive as a species, this is our moment! What do you say?
Are we going to be bees, or just Museum of Natural History keychains?
We're bees!
Keychain!
Then follow me! Except Keychain.

"""

def main():
    clean_text = TEXT.strip().upper().replace("\n", " ")
    add_text_to_json(TEXTS_PATH, clean_text)


def add_text_to_json(file_path, new_text):
    # Read the existing JSON file
    try:
        with open(TEXTS_PATH, 'r') as file:
            data = json.load(file)
            print(data)
    except FileNotFoundError:
        # If file does not exist, initialize with empty structure
        print("file not found")
        sys.exit(1)
    
    # Add the new text
    data["texts"].append(new_text)
    
    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    
    print(f'{new_text}\n\nText added successfully!')


if __name__ == "__main__":
    main()