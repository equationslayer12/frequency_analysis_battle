import re

def is_letter(letter):
    return re.match("^[a-zA-Z]$", letter) is not None

if __name__ == "__main__":
    print(is_letter('A'))