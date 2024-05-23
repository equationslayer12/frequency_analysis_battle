import { QUEUE, ONGOING, ENDED, COUNTDOWN, COUNTDOWN_TIME } from "@/Constants";
import TextState from "./TextState";
import { OpponentUser } from "@/user/OpponentUser";
import { ref, Ref } from "vue";


function removePunc(str: string) {
    return str.replace(/[^\w\s\']|_/g, "")
              .replace(/\s+/g, " ")
}


class Game {
    textState: TextState
    cipheredLettersCount: Ref<number>
    text: Ref<string>;
    cleanText: string;
    wordsArray: string[];
    status: Ref<string>;  // game status
    is_finished: Ref<boolean>;  // client status
    opponents: Ref<{[key: number]: OpponentUser}>;  // {username: OpponentUser}

    constructor() {
        this.textState = new TextState();
        this.cipheredLettersCount = ref(0);  // the amount of letters that are ciphered, the rest are not in the text.    
        this.text = ref('');
        this.cleanText = '';  // text without punctuation
        this.wordsArray = [];
        this.status = ref(QUEUE);
        this.is_finished = ref(false);
        this.opponents = ref({});
    }
    
    setTextLength(cipheredLettersCount: number) {
        this.cipheredLettersCount.value = cipheredLettersCount
    }

    setText(text: string, cipheredLettersCount: number) {
        text = text.toUpperCase();
        this.text.value = text;
        this.wordsArray = text.split(" ");
        this.cleanText = removePunc(text);

        this.cipheredLettersCount.value = cipheredLettersCount;
    }

    createOpponent(username: string, userId: number) {
        const newOpponent = new OpponentUser(username, userId);
        newOpponent.joinGame()
        this.opponents.value[userId] = newOpponent;
    }

    removeOpponent(userId: number) {
        delete this.opponents.value[userId];
    }

    /**
     * Sleeps for a couple of seconds, while setting the status to COUNTDOWN.
     */
    async startCountdown() {
        this.status.value = COUNTDOWN;
        return this.sleep(COUNTDOWN_TIME * 1000)  // this.sleep takes ms, and countdown time is in seconds.
    }

    /**
     * delay.
     * @param ms milliseconds to delay
     */
    async sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    start() {
        this.status.value = ONGOING;
        this.textState.reset();
    }

    changeLetter(fromLetter: string, toLetter: string) {
        const fromLetterState = this.textState.lettersState[fromLetter];
        const toLetterState = this.textState.lettersState[toLetter];
        toLetterState.value.otherLettersGuessedCount++;

        if (fromLetterState.value.isGuessed) {
            const changedLetter = fromLetterState.value.displayLetter
            const changedLetterState = this.textState.lettersState[changedLetter];
            changedLetterState.value.otherLettersGuessedCount--;
        }
        
        fromLetterState.value.isGuessed = true;
        fromLetterState.value.displayLetter = toLetter;
    }

    removeLetter(fromLetter: string) {
        const fromLetterState = this.textState.lettersState[fromLetter];
        if (!fromLetterState.value.isGuessed)
            return
        const deletedLetter: string = fromLetterState.value.displayLetter;
        const deletedLetterState = this.textState.lettersState[deletedLetter];

        deletedLetterState.value.otherLettersGuessedCount--;
        fromLetterState.value.displayLetter = fromLetter;
        fromLetterState.value.isGuessed = false;
    }

    /**
     * Client finished the game. game is still going (other players haven't finished)
     */
    finishGame() {
        this.textState.totalLettersGuessed.value = this.cipheredLettersCount.value;
        this.is_finished.value = true;
    }

    /**
     * Game has ended. Either by time limit or everybody finished.
     */
    endGame() {
        this.status.value = ENDED;
    }

    reset() {
        this.status.value = QUEUE;
        this.is_finished.value = false;
        this.setText("", 0);
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

export let cipheredLettersCount = game.cipheredLettersCount;  // the amount of letters that are ciphered, the rest are not in the text.    
export let gameStatus = game.status;
