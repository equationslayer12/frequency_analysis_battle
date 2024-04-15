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
    lettersGuessed: Ref<number>
    cipheredLettersCount: Ref<number>
    text: string
    wordsArray: string[]
    alphabet: string

    constructor() {
        this.selectedLetter = ref('');
        this.hiddenModeActive = ref(false);
        this.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        this.lettersState = ref({});
        this.letterBank = ref({});
        this.lettersGuessed = ref(0);
        this.cipheredLettersCount = ref(0);  // the amount of letters that are ciphered, the rest are not in the text.    
        for (let i = 0; i < this.alphabet.length; i++) {
            const letter = this.alphabet[i];
            this.lettersState.value[letter] = {'display': letter, 'isGuessed': false};
            this.letterBank.value[letter] = {'count': 0};
        }
        this.text = '';
        this.wordsArray = [];
    }

    /**
     * Reset text utils (letter bank, guessed letters, etc..)
     * don't reset text.
     */
    reset() {
        this.selectedLetter.value = '';
        this.hiddenModeActive.value = false;
        this.lettersState.value = {};
        this.letterBank.value = {};
        for (let i = 0; i < this.alphabet.length; i++) {
            const letter = this.alphabet[i];
            this.lettersState.value[letter] = {'display': letter, 'isGuessed': false};
            this.letterBank.value[letter] = {'count': 0};
        }
        this.lettersGuessed.value = 0;
        this.cipheredLettersCount.value = 0;  // the amount of letters that are ciphered, the rest are not in the text.    
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

let textUtil = new TextUtil();
export let letterBank = textUtil.letterBank;
export let lettersState = textUtil.lettersState;
export let selectedLetter = textUtil.selectedLetter;
export let hiddenModeActive = textUtil.hiddenModeActive;
export let lettersGuessed = textUtil.lettersGuessed;
export let cipheredLettersCount = textUtil.cipheredLettersCount;  // the amount of letters that are ciphered, the rest are not in the text.    

export default textUtil;

export function textUtilReset() {
    console.log("resettingg text util eeyyess");
    textUtil.reset();
}