import { Player } from './OpponentPlayer';
import User from './User';
import { cipheredLettersCount } from '@/game/Game';

/**
 * Represents an opponent user in the game.
 */
export class OpponentUser extends User {
     /**
      * The player associated with the opponent user.
      */
     player: Player | undefined;

     /**
      * The user ID of the opponent user.
      */
     userId: number;

     /**
      * Constructs an OpponentUser instance.
      * @param username The username of the opponent user.
      * @param userId The user ID of the opponent user.
      */
     constructor(username: string, userId: number) {
          super(username);
          this.player = undefined;
          this.userId = userId;
     }

     /**
      * Joins the game by creating a player instance for the opponent user.
      */
     joinGame() {
          this.player = new Player(
               this.username.value,
               cipheredLettersCount.value
          );
     }
}
