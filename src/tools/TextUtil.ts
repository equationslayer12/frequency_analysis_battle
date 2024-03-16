import {ref, Ref} from 'vue'

class TextUtil {
    selectedLetter: Ref<string>
    hiddenModeActive: Ref<boolean>
    lettersState: Ref<{[key: string]: object}>
    text: string
    wordsArray: string[]
    alphabet: string

    constructor() {
        this.selectedLetter = ref('');
        this.hiddenModeActive = ref(false);
        this.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        this.lettersState = ref({});
        for (let i = 0; i < this.alphabet.length; i++) {
            const letter = this.alphabet[i];
            this.lettersState.value[letter] = {'display': letter, 'isGuessed': false};
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

export default new TextUtil();
