import {ref, Ref} from 'vue'
import { alphabet } from '@/Constants'
import { LetterState } from './LetterState'

export default class TextState {
    selectedLetter: Ref<string>
    hiddenModeActive: Ref<boolean>
    /**
     * lettersState: if the user replaced a letter with another letter.
     * for example, if he replaced the letter P with R, it would look like this:
     * lettersState['P']  // LetterState<'display': 'R', isGuessed: true>
     */
    lettersState: {[key: string]: Ref<LetterState>}
    totalLettersGuessed: Ref<number>

    constructor() {
        this.selectedLetter = ref('');
        this.hiddenModeActive = ref(false);
        this.lettersState = {};
        this.totalLettersGuessed = ref(0);
        for (let i = 0; i < alphabet.length; i++) {
            const letter = alphabet[i];
            this.lettersState[letter] = ref(new LetterState(letter));
        }
    }

    selectLetter(newLetter: string, isAlphabet: boolean) {
        if (isAlphabet)
            this.selectedLetter.value = newLetter;
    }

    unselectLetter() {
        this.selectedLetter.value = '';
    }

    /**
     * Reset text utils (letter bank, guessed letters, etc..)
     * don't reset text.
     */
    reset() {
        this.selectedLetter.value = '';
        this.hiddenModeActive.value = false;
        for (let i = 0; i < alphabet.length; i++) {
            const letter = alphabet[i];
            const letterState = this.lettersState[letter];
            letterState.value.reset();
        }
        this.totalLettersGuessed.value = 0;
    }

    isLetter(letter: string) {
        return /^[A-Z]$/.test(letter);
    }
}
