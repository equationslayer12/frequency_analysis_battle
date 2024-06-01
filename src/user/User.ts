import { ref, Ref } from "vue";

/**
 * Signed up / guest user. 
 */
export default abstract class User {
    isGuest: Ref<boolean>
    username: Ref<string>
    constructor(username: string) {
        this.isGuest = ref(true);
        this.username = ref(username);
    }
}
