import { Player } from "./OpponentPlayer";
import User from "./User";
import { cipheredLettersCount } from "@/game/Game";

export class OpponentUser extends User {
    player: Player | undefined;

    constructor(username: string) {
        super(username);
        this.player = undefined;
    }

    joinGame() {
        this.player = new Player(this.username.value, cipheredLettersCount.value);
    }
};
