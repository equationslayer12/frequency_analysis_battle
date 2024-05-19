import { GameProgess } from "@/game/GameProgress";
import { ref, Ref } from "vue";

export class Player {
    username: Ref<string>;
    progress: GameProgess;

    constructor(username: string, textLength: number) {
        this.username = ref(username);
        this.progress = new GameProgess(textLength);
    }
}
