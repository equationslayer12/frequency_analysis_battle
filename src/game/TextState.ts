import { ref, Ref } from 'vue';
import { alphabet } from '@/Constants';
import { LetterState } from './LetterState';

/**
 * Represents the state of the text in the game.
 */
export default class TextState {
     /**
      * The currently selected letter.
      */
     selectedLetter: Ref<string>;

     /**
      * Indicates whether the hidden mode is active.
      */
     hiddenModeActive: Ref<boolean>;

     /**
      * The state of each letter in the alphabet.
      */
     lettersState: { [key: string]: Ref<LetterState> };

     /**
      * The total number of letters guessed by the player.
      */
     totalLettersGuessed: Ref<number>;

     /**
      * Creates a new instance of TextState.
      */
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

     /**
      * Selects a new letter.
      * @param newLetter The new letter to select.
      * @param isAlphabet Indicates whether the new letter is from the alphabet.
      */
     selectLetter(newLetter: string, isAlphabet: boolean): void {
          if (isAlphabet) this.selectedLetter.value = newLetter;
     }

     /**
      * Unselects the currently selected letter.
      */
     unselectLetter(): void {
          this.selectedLetter.value = '';
     }

     /**
      * Resets the text state.
      */
     reset(): void {
          this.selectedLetter.value = '';
          this.hiddenModeActive.value = false;
          for (let i = 0; i < alphabet.length; i++) {
               const letter = alphabet[i];
               const letterState = this.lettersState[letter];
               letterState.value.reset();
          }
          this.totalLettersGuessed.value = 0;
     }

     /**
      * Checks if a character is a letter.
      * @param letter The character to check.
      * @returns True if the character is a letter, otherwise false.
      */
     isLetter(letter: string): boolean {
          return /^[A-Z]$/.test(letter);
     }
}
