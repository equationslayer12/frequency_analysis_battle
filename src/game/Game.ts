/**
 * This class represents the game state and functionalities.
 * @module Game
 */

import { QUEUE, ONGOING, ENDED, COUNTDOWN, COUNTDOWN_TIME } from '@/Constants';
import TextState from './TextState';
import { OpponentUser } from '@/user/OpponentUser';
import { ref, Ref } from 'vue';

/**
 * Removes punctuation from a string.
 * @param {string} str - The input string.
 * @returns {string} - The string with punctuation removed.
 */
function removePunc(str: string): string {
     return str.replace(/[^\w\s\']|_/g, '').replace(/\s+/g, ' ');
}

/**
 * Represents the game state and functionalities.
 * @class
 */
class Game {
     textState: TextState;
     cipheredLettersCount: Ref<number>;
     text: Ref<string>;
     cleanText: string;
     wordsArray: string[];
     status: Ref<string>; // game status
     is_finished: Ref<boolean>; // client status
     opponents: Ref<{ [key: number]: OpponentUser }>; // {username: OpponentUser}

     /**
      * Creates an instance of Game.
      * @constructor
      */
     constructor() {
          this.textState = new TextState();
          this.cipheredLettersCount = ref(0); // the amount of letters that are ciphered, the rest are not in the text.
          this.text = ref('');
          this.cleanText = ''; // text without punctuation
          this.wordsArray = [];
          this.status = ref(QUEUE);
          this.is_finished = ref(false);
          this.opponents = ref({});
     }

     /**
      * Sets the number of ciphered letters.
      * @param {number} cipheredLettersCount - The number of ciphered letters.
      */
     setTextLength(cipheredLettersCount: number): void {
          this.cipheredLettersCount.value = cipheredLettersCount;
     }

     /**
      * Sets the text of the game.
      * @param {string} text - The text of the game.
      * @param {number} cipheredLettersCount - The number of ciphered letters.
      */
     setText(text: string, cipheredLettersCount: number): void {
          text = text.toUpperCase();
          this.text.value = text;
          this.wordsArray = text.split(' ');
          this.cleanText = removePunc(text);

          this.cipheredLettersCount.value = cipheredLettersCount;
     }

     /**
      * Creates a new opponent.
      * @param {string} username - The username of the opponent.
      * @param {number} userId - The user ID of the opponent.
      */
     createOpponent(username: string, userId: number): void {
          const newOpponent = new OpponentUser(username, userId);
          newOpponent.joinGame();
          this.opponents.value[userId] = newOpponent;
     }

     /**
      * Removes an opponent.
      * @param {number} userId - The user ID of the opponent to be removed.
      */
     removeOpponent(userId: number): void {
          delete this.opponents.value[userId];
     }

     /**
      * Starts the countdown for the game.
      * @returns {Promise<void>} - A promise that resolves after the countdown.
      */
     async startCountdown(): Promise<void> {
          this.status.value = COUNTDOWN;
          return this.sleep(COUNTDOWN_TIME * 1000); // this.sleep takes ms, and countdown time is in seconds.
     }

     /**
      * Delays the execution for a specified amount of time.
      * @param {number} ms - The number of milliseconds to delay.
      * @returns {Promise<void>} - A promise that resolves after the delay.
      */
     async sleep(ms: number): Promise<void> {
          return new Promise((resolve) => setTimeout(resolve, ms));
     }

     /**
      * Starts the game.
      */
     start(): void {
          this.status.value = ONGOING;
          this.textState.reset();
     }

     /**
      * Changes a letter in the text.
      * @param {string} fromLetter - The letter to change from.
      * @param {string} toLetter - The letter to change to.
      */
     changeLetter(fromLetter: string, toLetter: string): void {
          const fromLetterState = this.textState.lettersState[fromLetter];
          const toLetterState = this.textState.lettersState[toLetter];
          toLetterState.value.otherLettersGuessedCount++;

          if (fromLetterState.value.isGuessed) {
               const changedLetter = fromLetterState.value.displayLetter;
               const changedLetterState =
                    this.textState.lettersState[changedLetter];
               changedLetterState.value.otherLettersGuessedCount--;
          }

          fromLetterState.value.isGuessed = true;
          fromLetterState.value.displayLetter = toLetter;
     }

     /**
      * Removes a letter from the text.
      * @param {string} fromLetter - The letter to remove.
      */
     removeLetter(fromLetter: string): void {
          const fromLetterState = this.textState.lettersState[fromLetter];
          if (!fromLetterState.value.isGuessed) return;
          const deletedLetter: string = fromLetterState.value.displayLetter;
          const deletedLetterState = this.textState.lettersState[deletedLetter];

          deletedLetterState.value.otherLettersGuessedCount--;
          fromLetterState.value.displayLetter = fromLetter;
          fromLetterState.value.isGuessed = false;
     }

     /**
      * Finishes the game.
      */
     finishGame(): void {
          this.textState.totalLettersGuessed.value =
               this.cipheredLettersCount.value;
          this.is_finished.value = true;
     }

     /**
      * Ends the game.
      */
     endGame(): void {
          this.status.value = ENDED;
     }

     /**
      * Resets the game state.
      */
     reset(): void {
          this.status.value = QUEUE;
          this.is_finished.value = false;
          this.setText('', 0);
          this.textState.reset();
     }
}
export const game = new Game();

export let lettersState = game.textState.lettersState;
export let selectedLetter = game.textState.selectedLetter;
export let hiddenModeActive = game.textState.hiddenModeActive;
export let totalLettersGuessed = game.textState.totalLettersGuessed;
export let selectLetter = game.textState.selectLetter;
export let unselectLetter = game.textState.unselectLetter;
export let isLetter = game.textState.isLetter;
export let opponents = game.opponents;
export let cipheredLettersCount = game.cipheredLettersCount;
export let gameStatus = game.status;
