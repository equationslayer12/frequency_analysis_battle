import {ref, Ref} from 'vue'

class TextUtil {
    selectedLetter: Ref<string>
    hiddenModeActive: Ref<boolean>
    /**
     * lettersState: if the user replaced a letter with another letter.
     * for example, if he replaced the letter P with R, it would look like this:
     * lettersState['P']  // {'display': 'R', isGuessed: true} 
     */
    lettersState: Ref<{[key: string]: object}>
    /**
     * letterBank: counts how much each letter is guessed.
     * letterBank['P']  // {'count': 3}
     */
    letterBank: Ref<{[key: string]: object}>
    text: string
    wordsArray: string[]
    alphabet: string

    constructor() {
        this.selectedLetter = ref('');
        this.hiddenModeActive = ref(false);
        this.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        this.lettersState = ref({});
        this.letterBank = ref({});
        for (let i = 0; i < this.alphabet.length; i++) {
            const letter = this.alphabet[i];
            this.lettersState.value[letter] = {'display': letter, 'isGuessed': false};
            this.letterBank.value[letter] = {'count': 0};
        }
        this.text = '';
        this.wordsArray = [];
    
    }

    changeSelectedLetter(newLetter: string) {
        if (this.isLetter(newLetter) || newLetter == '')
            this.selectedLetter.value = newLetter;
    }

    isLetter(letter: string) {
        return /^[A-Z]$/.test(letter);
    }
    
    setText(text: string) {
        this.text = text;
        this.wordsArray = text.split(" ");
    }
}

const textUtil = new TextUtil();
export const letterBank = textUtil.letterBank;
export const lettersState = textUtil.lettersState;
export const selectedLetter = textUtil.selectedLetter;
export const hiddenModeActive = textUtil.hiddenModeActive;

export default textUtil;
