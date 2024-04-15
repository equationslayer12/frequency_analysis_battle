export default class Protocol {
    static deleteChar: string = "del";
    static GAME_ENDED: string = "end";
    
    static Request = class {
        static newText = "new";  // request a new text
        static changeLetter(originLetter: string, gussedLetter: string) {
            return `CL;${originLetter};${gussedLetter}`
        }
    }
}