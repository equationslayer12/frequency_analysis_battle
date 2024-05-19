import { ref, Ref } from "vue";

/**
 * Signed up / guest user. 
 */
export default abstract class User {
    isGuest: boolean
    username: Ref<string>
    constructor(username: string) {
        this.isGuest = true;
        this.username = ref(username);
    }
}
