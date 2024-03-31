export default class Protocol {
    static Encrypt = class {
        static changeLetter(originLetter: string, gussedLetter: string) {
            return `CL;${originLetter};${gussedLetter}`
    }
 
    }
}