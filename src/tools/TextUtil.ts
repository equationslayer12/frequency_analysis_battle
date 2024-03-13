import {ref, Ref} from 'vue'

class TextUtil {
    selectedLetter: Ref<string>
    hiddenModeActive: Ref<boolean>
    lettersState: Ref<object>
    text: string
    wordsArray: string[]
    alphabet: string

    constructor() {
        this.selectedLetter = ref('');
        this.hiddenModeActive = ref(false);
        this.lettersState = ref({
            'A': { 'display': 'A', 'isGuessed': false }, 'B': { 'display': 'B', 'isGuessed': false }, 'C': { 'display': 'C', 'isGuessed': false }, 'D': { 'display': 'D', 'isGuessed': false }, 'E': { 'display': 'E', 'isGuessed': false }, 'F': { 'display': 'F', 'isGuessed': false }, 'G': { 'display': 'G', 'isGuessed': false }, 'H': { 'display': 'H', 'isGuessed': false }, 'I': { 'display': 'I', 'isGuessed': false }, 'J': { 'display': 'J', 'isGuessed': false }, 'K': { 'display': 'K', 'isGuessed': false }, 'L': { 'display': 'L', 'isGuessed': false }, 'M': { 'display': 'M', 'isGuessed': false }, 'N': { 'display': 'N', 'isGuessed': false }, 'O': { 'display': 'O', 'isGuessed': false }, 'P': { 'display': 'P', 'isGuessed': false }, 'Q': { 'display': 'Q', 'isGuessed': false }, 'R': { 'display': 'R', 'isGuessed': false }, 'S': { 'display': 'S', 'isGuessed': false }, 'T': { 'display': 'T', 'isGuessed': false }, 'U': { 'display': 'U', 'isGuessed': false }, 'V': { 'display': 'V', 'isGuessed': false }, 'W': { 'display': 'W', 'isGuessed': false }, 'X': { 'display': 'X', 'isGuessed': false }, 'Y': { 'display': 'Y', 'isGuessed': false }, 'Z': { 'display': 'Z', 'isGuessed': false }, 
        });
        this.text = '';
        this.wordsArray = [];
        this.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
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
