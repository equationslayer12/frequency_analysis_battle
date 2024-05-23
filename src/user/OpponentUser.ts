import { Player } from "./OpponentPlayer";
import User from "./User";
import { cipheredLettersCount } from "@/game/Game";

export class OpponentUser extends User {
    player: Player | undefined;
    userId: number;
    
    constructor(username: string, userId: number) {
        super(username);
        this.player = undefined;
        this.userId = userId;
    }

    joinGame() {
        this.player = new Player(this.username.value, cipheredLettersCount.value);
    }
};
