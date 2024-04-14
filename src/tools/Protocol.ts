export default class Protocol {
    static deleteChar: string = "del";
    static GAME_ENDED: string = "end";
    
    static Encrypt = class {
        static changeLetter(originLetter: string, gussedLetter: string) {
            return `CL;${originLetter};${gussedLetter}`
    }
 
    }
}