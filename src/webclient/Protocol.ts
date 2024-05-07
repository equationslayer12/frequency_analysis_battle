export default class Protocol {
    static deleteChar: string = "del";
    static GAME_ENDED: string = "end";
    static success: string = "success";
    
    static Request = class {
        static newText = "new";  // request a new text
        static changeLetter(originLetter: string, gussedLetter: string) {
            return `CL;${originLetter};${gussedLetter}`
        }
    };

    static Sessions = class {
        static decryptUsername(username: string) {
            return username;
        };
        static encryptUsername(username: string) {
            return username;
        };    
    };
}