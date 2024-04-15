import SessionUtils from "./SessionUtils";
import { ref, Ref } from "vue";

class User {
    isGuest: boolean
    username: Ref<string>
    constructor(username: string) {
        this.isGuest = true;
        this.username = ref(username);
    }

    /**
     * Updates username from the username cookie. it is changeable by the user,
     * but it should'nt be a big deal. unless?
     */
    updateFromCookie() {
        let username = SessionUtils.getCookie("username");
        if (!username)
            return;
        this.username.value = SessionUtils.decryptUsername(username);
    }

    logIn() {
        this.updateFromCookie();
        this.isGuest = false;
    }

    logOut() {
        this.username.value = defaultUsername;
        this.isGuest = true;
    }

}

const defaultUsername = "Guest"
console.log('chaning to guest...');
const clientUser = new User(defaultUsername);
export default clientUser;

export const username = clientUser.username;
