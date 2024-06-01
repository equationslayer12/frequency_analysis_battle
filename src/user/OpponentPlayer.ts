import { GameProgress } from '@/game/GameProgress';
import { ref, Ref } from 'vue';

/**
 * Represents a player in the game.
 */
export class Player {
     /**
      * The username of the player.
      */
     username: Ref<string>;

     /**
      * The game progress of the player.
      */
     progress: GameProgress;

     /**
      * Constructs a Player instance.
      * @param username The username of the player.
      * @param textLength The length of the text for the game progress.
      */
     constructor(username: string, textLength: number) {
          this.username = ref(username);
          this.progress = new GameProgress(textLength);
     }
}
