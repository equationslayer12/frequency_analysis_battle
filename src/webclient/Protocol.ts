export default class Protocol {
    static success: string = "success";
    static deleteChar: string = "del";
    static GAME_ENDED: string = "end";
    static FINISHED: number = -1;
    
    static SPLIT = ";";

    static Request = class {
        static textLength = "len"; // request the text length
        static newText = "new";  // request a new text
        static text = "text";  // request the text in a multiplayer lobby
        static syncData = "sync";  // request all players progress
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

        static sync(response: string) {
            const parts = response.split(Protocol.SPLIT);
            const gameStatus = parts[0];
            const userIds: number[] = [];
            const scores: number[] = [];
    
            for (let i = 1; i < parts.length; i += 2) {
                const userId = parts[i];
                const score = parts[i + 1];
                userIds.push(Number(userId));
                scores.push(Number(score));
            }
    
            return { gameStatus, userIds, scores };
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