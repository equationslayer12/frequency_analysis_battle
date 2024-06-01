from dataclasses import dataclass
import string
import random
from backend.config.constants import TEXTS_PATH
from backend.utils.string_utils import is_letter
import json

# temp_text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…"
# temp_text = "THIS IS A TESTING TEXT SENT BY THE API"
# temp_text = "API"
temp_text = "IT IS A PERIOD OF CIVIL WAR. REBEL SPACESHIPS, STRIKING FROM A HIDDEN BASE, HAVE WON THEIR FIRST VICTORY AGAINST THE EVIL GALACTIC EMPIRE. DURING THE BATTLE, REBEL SPIES MANAGED TO STEAL SECRET PLANS TO THE EMPIRE’S ULTIMATE WEAPON, THE DEATH STAR, AN ARMORED SPACE STATION WITH ENOUGH POWER TO DESTROY AN ENTIRE PLANET. PURSUED BY THE EMPIRE’S SINISTER AGENTS, PRINCESS LEIA RACES HOME ABOARD HER STARSHIP, CUSTODIAN OF THE STOLEN PLANS THAT CAN SAVE HER PEOPLE AND RESTORE FREEDOM TO THE GALAXY…"
# temp_text = """Out too the been like hard off. Improve enquire welcome own beloved matters her. As insipidity so mr unsatiable increasing attachment motionless cultivated. Addition mr husbands unpacked occasion he oh. Is unsatiable if projecting boisterous insensible. It recommend be resolving pretended middleton. Is he staying arrival address earnest. To preference considered it themselves inquietude collecting estimating. View park for why gay knew face. Next than near to four so hand. Times so do he downs me would. Witty abode party her found quiet law. They door four bed fail now have.""".upper()
temp_text = temp_text.upper()

def get_texts():
    """
    Load texts from a JSON file.

    Returns:
        list: A list of texts.
    """
    with open(TEXTS_PATH) as file:
        data = json.load(file)
        return data['texts']

@dataclass
class CipherObject:
    """
    A class to represent a ciphered text and its decipher dictionary.

    Attributes:
        text (str): The ciphered text.
        decipher_dictionary (dict): A dictionary to map ciphered letters back to original letters.
    """
    text: str
    decipher_dictionary: dict

class TextHandler:
    """
    A class to handle text operations including getting random text and ciphering text.
    """
    def __init__(self) -> None:
        """
        Initialize the TextHandler with texts loaded from the database.
        """
        self.texts = get_texts()

    def get_random_ciphered_text(self) -> CipherObject:
        """
        Get a random text and cipher it.

        Returns:
            CipherObject: The ciphered text and its decipher dictionary.
        """
        return self.cipher_text(
            text=self.get_random_text()
        )

    def cipher_text(self, text: str) -> CipherObject:
        """
        Cipher the given text by substituting each letter with a randomly shuffled letter.

        Args:
            text (str): The text to be ciphered.

        Returns:
            CipherObject: The ciphered text and its decipher dictionary.
        """
        shuffled_letters = list(string.ascii_uppercase)
        random.shuffle(shuffled_letters)

        cipher_dictionary = {}
        decipher_dictionary = {}

        ciphered_text = ""
        i = 0
        for letter in text:
            if not is_letter(letter):
                ciphered_text += letter
                continue

            if letter not in cipher_dictionary:
                random_letter = shuffled_letters[i]
                i += 1
                cipher_dictionary[letter] = random_letter
                decipher_dictionary[random_letter] = letter

            ciphered_letter = cipher_dictionary.get(letter)
            ciphered_text += ciphered_letter

        return CipherObject(ciphered_text, decipher_dictionary)

    def get_random_text(self) -> str:
        """
        Choose a random text from the database.

        Returns:
            str: A randomly chosen text.
        """
        return random.choice(self.texts)
