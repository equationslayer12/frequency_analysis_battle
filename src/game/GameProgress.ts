import { Ref, ref } from "vue";

export class GameProgess {
    current: Ref<number>;
    end: Ref<number>;

    constructor(textLength: number) {
        this.current = ref(0);
        this.end = ref(textLength);
    }

    add(amount=1) {
        this.current.value += amount;
    }
}