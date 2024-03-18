from dataclasses import dataclass
import string
import random

temp_text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…"
# temp_text = "THIS IS A TESTING TEXT SENT BY THE API"


@dataclass
class CipherObject:
    text: str
    dictionary: dict


class TextHandler:
    def get_random_ciphered_text(self) -> str:
        return self.cipher_text(
            text=self.get_random_text()
        )

    def cipher_text(self, text: str) -> CipherObject:

        all_letters = list(string.ascii_uppercase)
        shuffled_letters = list(string.ascii_uppercase)
        random.shuffle(shuffled_letters)

        dictionary = {
            letter: random_letter for letter, random_letter in zip(all_letters, shuffled_letters)
        }

        ciphered_text = ""
        for letter in text:
            ciphered_letter = dictionary.get(letter)
            if ciphered_letter is None:
                ciphered_letter = letter
            ciphered_text += ciphered_letter

        return CipherObject(ciphered_text, dictionary)

    def get_random_text(self) -> str:
        return temp_text
