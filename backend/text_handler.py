from dataclasses import dataclass
import string
import random
from utils import is_letter

# temp_text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…"
# temp_text = "THIS IS A TESTING TEXT SENT BY THE API"
# temp_text = "API"
temp_text = "IT IS A PERIOD OF CIVIL WAR. REBEL SPACESHIPS, STRIKING FROM A HIDDEN BASE, HAVE WON THEIR FIRST VICTORY AGAINST THE EVIL GALACTIC EMPIRE. DURING THE BATTLE, REBEL SPIES MANAGED TO STEAL SECRET PLANS TO THE EMPIRE’S ULTIMATE WEAPON, THE DEATH STAR, AN ARMORED SPACE STATION WITH ENOUGH POWER TO DESTROY AN ENTIRE PLANET. PURSUED BY THE EMPIRE’S SINISTER AGENTS, PRINCESS LEIA RACES HOME ABOARD HER STARSHIP, CUSTODIAN OF THE STOLEN PLANS THAT CAN SAVE HER PEOPLE AND RESTORE FREEDOM TO THE GALAXY…"
# temp_text = """Out too the been like hard off. Improve enquire welcome own beloved matters her. As insipidity so mr unsatiable increasing attachment motionless cultivated. Addition mr husbands unpacked occasion he oh. Is unsatiable if projecting boisterous insensible. It recommend be resolving pretended middleton. Is he staying arrival address earnest. To preference considered it themselves inquietude collecting estimating. View park for why gay knew face. Next than near to four so hand. Times so do he downs me would. Witty abode party her found quiet law. They door four bed fail now have.""".upper()

@dataclass
class CipherObject:
    """ciphered text.
    text: chipered text
    dictionary: a decipher dictionary. {ciphered_letter: original_letter}
    """
    text: str
    decipher_dictionary: dict


class TextHandler:
    def get_random_ciphered_text(self) -> str:
        return self.cipher_text(
            text=self.get_random_text()
        )

    def cipher_text(self, text: str) -> CipherObject:
        shuffled_letters = list(string.ascii_uppercase)
        random.shuffle(shuffled_letters)

        cipher_dictionary = {}
        decipher_dictionary = {}

        ciphered_text = ""
        i = 0
        for letter in text:  # cipher every letter
            if not is_letter(letter):
                ciphered_text += letter
                continue
                

            if letter not in cipher_dictionary:
                # if letter hasn't been ciphered yet
                random_letter = shuffled_letters[i]
                i += 1
                cipher_dictionary[letter] = random_letter
                decipher_dictionary[random_letter] = letter

            ciphered_letter = cipher_dictionary.get(letter)
            ciphered_text += ciphered_letter

        return CipherObject(ciphered_text, decipher_dictionary)

    def get_random_text(self) -> str:
        """Choose a random text from the db.

        Returns:
            str: text
        """
        return temp_text
