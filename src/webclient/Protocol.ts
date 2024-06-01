/**
 * Utility class defining the protocol used for communication between client and server.
 */
export default class Protocol {
     /** Represents a successful operation. */
     static success: string = 'success';

     /** Represents a request to delete a character. */
     static deleteChar: string = 'del';

     /** Indicates that the game has ended. */
     static GAME_ENDED: string = 'end';

     /** Represents a finished state. */
     static FINISHED: number = -1;

     /** Separator used for splitting protocol messages. */
     static SPLIT = ';';

     /** Contains various types of request messages. */
     static Request = class {
          /** Requests the text length. */
          static textLength = 'len';

          /** Requests a new text. */
          static newText = 'new';

          /** Requests the text in a multiplayer lobby. */
          static text = 'text';

          /** Requests synchronization data for all players' progress. */
          static syncData = 'sync';

          /**
           * Creates a change letter request message.
           * @param originLetter The original letter.
           * @param guessedLetter The guessed letter.
           * @returns The formatted change letter request message.
           */
          static changeLetter(
               originLetter: string,
               guessedLetter: string
          ): string {
               return `CL${Protocol.SPLIT}${originLetter}${Protocol.SPLIT}${guessedLetter}`;
          }
     };

     /** Contains various types of response messages. */
     static Response = class {
          /**
           * Splits a response message into parts using the protocol separator.
           * @param response The response message to split.
           * @returns An array of parts.
           */
          static splitResponse(response: string): string[] {
               return response.split(Protocol.SPLIT);
          }

          /**
           * Extracts the text length from a response message.
           * @param response The response message containing the text length.
           * @returns The extracted text length.
           */
          static textLength(response: string): number {
               return parseInt(response);
          }

          /**
           * Parses synchronization data from a response message.
           * @param response The response message containing synchronization data.
           * @returns An object containing game status, user IDs, and scores.
           */
          static sync(response: string): {
               gameStatus: string;
               userIds: number[];
               scores: number[];
          } {
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

          /** Contains various types of event messages. */
          static Event = class {
               /** Indicates an update to existing players. */
               static UpdateExistingPlayers = 'UEP';

               /** Indicates that a player has joined the game. */
               static PlayerJoined = 'PJ';

               /** Indicates that a player has left the game. */
               static PlayerLeft = 'PL';

               /** Indicates the start of a countdown. */
               static StartCountdown = 'SC';
          };
     };

     /** Contains utility methods related to sessions. */
     static Sessions = class {
          /**
           * Decrypts a username.
           * @param username The encrypted username.
           * @returns The decrypted username.
           */
          static decryptUsername(username: string): string {
               return username;
          }

          /**
           * Encrypts a username.
           * @param username The username to encrypt.
           * @returns The encrypted username.
           */
          static encryptUsername(username: string): string {
               return username;
          }
     };
}
