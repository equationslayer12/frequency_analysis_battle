/**
 * Represents the state of a letter in the game.
 */
export class LetterState {
     /**
      * The original letter.
      */
     letter: string;

     /**
      * The letter to be displayed.
      */
     displayLetter: string;

     /**
      * Indicates whether the letter has been guessed.
      */
     isGuessed: boolean;

     /**
      * The number of other letters changed to this one.
      */
     otherLettersGuessedCount: number;

     /**
      * Creates a new instance of LetterState.
      * @param letter The original letter.
      */
     constructor(letter: string) {
          this.letter = letter;
          this.displayLetter = this.letter;
          this.isGuessed = false;
          this.otherLettersGuessedCount = 0;
     }

     /**
      * Resets the letter state to its initial values.
      */
     reset(): void {
          this.displayLetter = this.letter;
          this.isGuessed = false;
          this.otherLettersGuessedCount = 0;
     }
}
