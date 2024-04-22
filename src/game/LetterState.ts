
export class LetterState {
    letter: string;
    displayLetter: string;
    isGuessed: boolean;
    otherLettersGuessedCount: number;  // Amount of other letters changed to this one

    constructor(letter: string) {
        this.letter = letter;
        this.displayLetter = this.letter;
        this.isGuessed = false;
        this.otherLettersGuessedCount = 0;
    }

    reset() {
        this.displayLetter = this.letter;
        this.isGuessed = false;
        this.otherLettersGuessedCount = 0;
    }
}