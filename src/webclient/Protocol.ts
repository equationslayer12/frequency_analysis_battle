export default class Protocol {
    static deleteChar: string = "del";
    static GAME_ENDED: string = "end";
    static success: string = "success";
    
    static SPLIT = ";";

    static Request = class {
        static textLength = "len"; // request the text length
        static newText = "new";  // request a new text
        static text = "text";  // request the text in a multiplayer lobby
        static changeLetter(originLetter: string, gussedLetter: string) {
            return `CL${Protocol.SPLIT}${originLetter}${Protocol.SPLIT}${gussedLetter}`
        }
    };

    static Response = class {
        static splitResponse(response: string): string[] {
            return response.split(Protocol.SPLIT)
        }

        static textLength(response: string): number {
            return parseInt(response);
        }

        static Event = class {
            static UpdateExistingPlayers = "UEP";
            static PlayerJoined = "PJ";
            static PlayerLeft = "PL";
            static StartCountdown = "SC";
        }
    }

    static Sessions = class {
        static decryptUsername(username: string) {
            return username;
        };
        static encryptUsername(username: string) {
            return username;
        };    
    };
}