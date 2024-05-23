import { Ref, ref } from "vue";

export class GameProgess {
    current: Ref<number> | number;
    end: Ref<number>;

    constructor(textLength: number) {
        this.current = ref(0);
        this.end = ref(textLength);
    }
}